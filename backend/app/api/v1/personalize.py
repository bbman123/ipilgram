import logging
import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.api.deps import require_role
from app.core.database import get_db
from app.core.rate_limit import limiter
from app.schemas.response import success_response
from app.models.user import User, Role
from app.schemas.personalize import (
    SimplifyRequest,
    SimplifyResponse,
    TranslateRequest,
    TranslateResponse,
    ProcessRequest,
    ProcessResponse,
    PilgrimQueryRequest,
    AIQueryResponse,
    HealthCheckResponse,
)
from app.services.ai.gemini import GeminiProvider
from app.services.ai.engine import PersonalizationEngine
from app.services.tts import generate_audio

logger = logging.getLogger("hajj_api")

router = APIRouter(prefix="/personalize", tags=["AI Personalization"])


def _get_engine() -> PersonalizationEngine:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GEMINI_API_KEY not configured. AI personalization is unavailable.",
        )
    provider = GeminiProvider(api_key)
    return PersonalizationEngine(provider)


# ---------------------------------------------------------------------------
# Pilgrim-scoped: AI answers from the pilgrim's own authorized context
# ---------------------------------------------------------------------------

@router.post(
    "/ask",
    summary="Ask a question about your Hajj data",
    description=(
        "Pilgrim sends a question. Backend builds context from their own "
        "package, flight, accommodation, transport, and announcements, then "
        "sends it to AI. AI can only see the pilgrim's own data."
    ),
    responses={
        200: {"description": "AI response based on pilgrim's own data"},
        401: {"description": "Authentication required"},
        403: {"description": "Pilgrim role required"},
        503: {"description": "AI provider not configured"},
        502: {"description": "AI provider error"},
    },
)
@limiter.limit("20/minute")
def ask_ai(
    body: PilgrimQueryRequest,
    request: Request,
    pilgrim: Annotated[User, Depends(require_role(Role.pilgrim))],
    db: Annotated[object, Depends(get_db)],
):
    engine = _get_engine()
    try:
        result = engine.answer_query(pilgrim.id, body.query, db)
    except Exception as e:
        logger.error("AI ask error: pilgrim=%d: %s", pilgrim.id, str(e))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI provider error. Please try again later.",
        )

    return success_response(data=AIQueryResponse(**result).model_dump(), message="AI response generated")


@router.post(
    "/ask/audio",
    summary="Ask a question and get audio response",
    description=(
        "Same as /ask but also generates audio via gTTS. "
        "The audio file is returned as a streaming response."
    ),
    responses={
        200: {"description": "Audio file (MP3)"},
        401: {"description": "Authentication required"},
        403: {"description": "Pilgrim role required"},
        502: {"description": "AI provider error"},
        503: {"description": "AI provider or TTS not configured"},
    },
)
@limiter.limit("10/minute")
def ask_ai_audio(
    body: PilgrimQueryRequest,
    request: Request,
    pilgrim: Annotated[User, Depends(require_role(Role.pilgrim))],
    db: Annotated[object, Depends(get_db)],
):
    engine = _get_engine()
    try:
        result = engine.answer_query(pilgrim.id, body.query, db)
    except Exception as e:
        logger.error("AI ask+audio error: pilgrim=%d: %s", pilgrim.id, str(e))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI provider error. Please try again later.",
        )

    language = result.get("language", "English")
    tts_map = {"English": "en", "Hausa": "ha", "Arabic": "ar", "Yoruba": "yo", "Igbo": "ig"}
    lang_code = tts_map.get(language, "en")

    from app.services.tts import AUDIO_CACHE_DIR
    audio_url = generate_audio(result["response"], lang_code)
    if not audio_url:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="TTS generation failed. Audio unavailable.",
        )

    import hashlib
    key = hashlib.sha256(f"{result['response']}:{lang_code}".encode()).hexdigest()
    filepath = AUDIO_CACHE_DIR / f"{key}.mp3"
    if not filepath.exists():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="TTS generation failed. Audio file not found.",
        )

    from fastapi.responses import FileResponse
    return FileResponse(str(filepath), media_type="audio/mpeg", filename="response.mp3")


# ---------------------------------------------------------------------------
# Admin-only: backward-compatible endpoints for direct text processing
# ---------------------------------------------------------------------------

@router.post(
    "/simplify",
    summary="Simplify announcement text",
    description="Use AI to rewrite a Hajj announcement in plain, easy-to-understand language.",
    responses={
        200: {"description": "Simplified text returned"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        503: {"description": "AI provider not configured"},
        502: {"description": "AI provider error"},
    },
)
def simplify_announcement(
    body: SimplifyRequest,
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    engine = _get_engine()
    try:
        result = engine.simplify(body.text, body.language.value)
    except Exception as e:
        logger.error("AI simplify error: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI provider error. Please try again later.",
        )

    return success_response(
        data=SimplifyResponse(
            original=body.text,
            simplified=result["response"],
            language=body.language.value,
            model_used="",
        ).model_dump(),
        message="Text simplified successfully",
    )


@router.post(
    "/translate",
    summary="Translate announcement text",
    description="Translate Hajj information between supported languages using AI.",
    responses={
        200: {"description": "Translated text returned"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        503: {"description": "AI provider not configured"},
        502: {"description": "AI provider error"},
    },
)
def translate_announcement(
    body: TranslateRequest,
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    engine = _get_engine()
    try:
        result = engine.translate(
            body.text,
            body.target_language.value,
            body.source_language.value,
        )
    except Exception as e:
        logger.error("AI translate error: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI provider error. Please try again later.",
        )

    return success_response(
        data=TranslateResponse(
            original=body.text,
            translated=result["response"],
            source_language=body.source_language.value,
            target_language=body.target_language.value,
            model_used="",
        ).model_dump(),
        message="Text translated successfully",
    )


@router.post(
    "/process",
    summary="Full AI processing pipeline",
    description="Run the complete personalization pipeline: simplify text, translate to target language, and optionally prepare audio output.",
    responses={
        200: {"description": "Processed result returned"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        503: {"description": "AI provider not configured"},
        502: {"description": "AI provider error"},
    },
)
def process_announcement(
    body: ProcessRequest,
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    engine = _get_engine()
    try:
        result = engine.process(
            body.text,
            body.target_language.value,
            body.audio_required,
        )
    except Exception as e:
        logger.error("AI process error: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI provider error. Please try again later.",
        )

    return success_response(data=ProcessResponse(**result).model_dump(), message="Announcement processed successfully")


@router.get(
    "/health",
    summary="Check AI provider status",
    description="Verify if the AI personalization provider (Gemini) is configured and available.",
    responses={
        200: {"description": "AI provider status"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def ai_health(
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    api_key = os.environ.get("GEMINI_API_KEY", "")
    return success_response(
        data=HealthCheckResponse(
            provider="gemini",
            configured=bool(api_key),
        ).model_dump(),
        message="AI health check completed",
    )
