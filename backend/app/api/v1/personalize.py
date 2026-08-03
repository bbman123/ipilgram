import logging
import traceback

from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.api.deps import require_role
from app.core.config import get_settings
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
from app.services.ai.gemini import GeminiProvider, GeminiError
from app.services.ai.engine import PersonalizationEngine
from app.services.tts import generate_audio

logger = logging.getLogger("hajj_api")

router = APIRouter(prefix="/personalize", tags=["AI Personalization"])


def _get_engine() -> PersonalizationEngine:
    settings = get_settings()
    api_key = settings.GEMINI_API_KEY

    logger.info(
        "AI config: enabled=%s, model=%s, api_key_exists=%s, api_key_length=%s, provider=gemini, timeout=30, temperature=0.3, max_tokens=2048",
        bool(api_key),
        "gemini-3.5-flash",
        bool(api_key),
        len(api_key) if api_key else 0,
    )

    if not api_key:
        return None
    return PersonalizationEngine(GeminiProvider(api_key))


def _ai_error_response(e: GeminiError):
    """Map GeminiError to a JSON error response."""
    return {
        "success": False,
        "message": e.message,
        "data": None,
        "errors": e.details,
    }


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
    logger.info("Entering /ask: pilgrim_id=%d, query=%r", pilgrim.id, body.query[:100])

    engine = _get_engine()
    if engine is None:
        return _ai_error_response(GeminiError(
            message="AI service is not configured. Please contact the administrator.",
            status_code=503,
            details={"reason": "not_configured"},
        ))
    try:
        result = engine.answer_query(pilgrim.id, body.query, db)
    except GeminiError as e:
        logger.error("Gemini error on /ask: pilgrim=%d, reason=%s", pilgrim.id, e.details.get("reason", "unknown"))
        return _ai_error_response(e)
    except Exception as e:
        logger.error("Unexpected error on /ask: pilgrim=%d: %s", pilgrim.id, str(e))
        logger.error("Full traceback on /ask:\n%s", traceback.format_exc())
        return _ai_error_response(GeminiError(
            message="An unexpected error occurred. Please try again later.",
            status_code=500,
            details={"reason": "internal_error", "error": str(e)[:200]},
        ))

    logger.info("Returning /ask result: success=True, category=%s", result.get("category"))
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
    if engine is None:
        return _ai_error_response(GeminiError(
            message="AI service is not configured. Please contact the administrator.",
            status_code=503,
            details={"reason": "not_configured"},
        ))
    try:
        result = engine.answer_query(pilgrim.id, body.query, db)
    except GeminiError as e:
        logger.error("Gemini error on /ask/audio: pilgrim=%d, reason=%s", pilgrim.id, e.details.get("reason", "unknown"))
        return _ai_error_response(e)
    except Exception as e:
        logger.error("Unexpected error on /ask/audio: pilgrim=%d: %s", pilgrim.id, str(e))
        logger.error("Full traceback on /ask/audio:\n%s", traceback.format_exc())
        return _ai_error_response(GeminiError(
            message="An unexpected error occurred. Please try again later.",
            status_code=500,
            details={"reason": "internal_error", "error": str(e)[:200]},
        ))

    language = result.get("language", "English")

    from app.services.tts import AUDIO_CACHE_DIR
    audio_url = generate_audio(result["response"], language)
    if not audio_url:
        return _ai_error_response(GeminiError(
            message="Audio generation failed. Please try again later.",
            status_code=503,
            details={"reason": "tts_failed"},
        ))

    import hashlib
    from app.services.tts import _resolve_lang_code
    lang_code = _resolve_lang_code(language)
    key = hashlib.sha256(f"{result['response']}:{lang_code}".encode()).hexdigest()
    filepath = AUDIO_CACHE_DIR / f"{key}.mp3"
    if not filepath.exists():
        return _ai_error_response(GeminiError(
            message="Audio file could not be created.",
            status_code=503,
            details={"reason": "tts_file_missing"},
        ))

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
    if engine is None:
        return _ai_error_response(GeminiError(
            message="AI service is not configured. Please contact the administrator.",
            status_code=503,
            details={"reason": "not_configured"},
        ))
    try:
        result = engine.simplify(body.text, body.language.value)
    except GeminiError as e:
        logger.error("Gemini error on /simplify: %s", e.details.get("reason", "unknown"))
        return _ai_error_response(e)
    except Exception as e:
        logger.error("Unexpected error on /simplify: %s", str(e))
        return _ai_error_response(GeminiError(
            message="An unexpected error occurred. Please try again later.",
            status_code=500,
            details={"reason": "internal_error", "error": str(e)[:200]},
        ))

    return success_response(
        data=SimplifyResponse(
            original=body.text,
            simplified=result["response"],
            language=body.language.value,
            model_used="gemini-3.5-flash",
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
    if engine is None:
        return _ai_error_response(GeminiError(
            message="AI service is not configured. Please contact the administrator.",
            status_code=503,
            details={"reason": "not_configured"},
        ))
    try:
        result = engine.translate(
            body.text,
            body.target_language.value,
            body.source_language.value,
        )
    except GeminiError as e:
        logger.error("Gemini error on /translate: %s", e.details.get("reason", "unknown"))
        return _ai_error_response(e)
    except Exception as e:
        logger.error("Unexpected error on /translate: %s", str(e))
        return _ai_error_response(GeminiError(
            message="An unexpected error occurred. Please try again later.",
            status_code=500,
            details={"reason": "internal_error", "error": str(e)[:200]},
        ))

    return success_response(
        data=TranslateResponse(
            original=body.text,
            translated=result["response"],
            source_language=body.source_language.value,
            target_language=body.target_language.value,
            model_used="gemini-3.5-flash",
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
    if engine is None:
        return _ai_error_response(GeminiError(
            message="AI service is not configured. Please contact the administrator.",
            status_code=503,
            details={"reason": "not_configured"},
        ))
    try:
        result = engine.process(
            body.text,
            body.target_language.value,
            body.audio_required,
        )
    except GeminiError as e:
        logger.error("Gemini error on /process: %s", e.details.get("reason", "unknown"))
        return _ai_error_response(e)
    except Exception as e:
        logger.error("Unexpected error on /process: %s", str(e))
        return _ai_error_response(GeminiError(
            message="An unexpected error occurred. Please try again later.",
            status_code=500,
            details={"reason": "internal_error", "error": str(e)[:200]},
        ))

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
    settings = get_settings()
    api_key = settings.GEMINI_API_KEY
    return success_response(
        data=HealthCheckResponse(
            provider="gemini",
            configured=bool(api_key),
        ).model_dump(),
        message="AI health check completed",
    )
