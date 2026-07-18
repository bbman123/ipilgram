import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.api.deps import require_role
from app.models.user import User, Role
from app.schemas.personalize import (
    SimplifyRequest,
    SimplifyResponse,
    TranslateRequest,
    TranslateResponse,
    ProcessRequest,
    ProcessResponse,
)
from app.services.ai.gemini import GeminiProvider
from app.services.ai.engine import PersonalizationEngine

router = APIRouter(prefix="/personalize", tags=["AI Personalization"])


def _get_engine() -> PersonalizationEngine:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GEMINI_API_KEY not configured",
        )
    provider = GeminiProvider(api_key)
    return PersonalizationEngine(provider)


@router.post("/simplify", response_model=SimplifyResponse)
def simplify_announcement(
    body: SimplifyRequest,
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    """Simplify a Hajj announcement into plain, clear language."""
    engine = _get_engine()
    try:
        result = engine.simplify(body.text, body.language.value)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI provider error: {str(e)}",
        )

    return SimplifyResponse(
        original=body.text,
        simplified=result.text,
        language=body.language.value,
        model_used=result.model,
    )


@router.post("/translate", response_model=TranslateResponse)
def translate_announcement(
    body: TranslateRequest,
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    """Translate Hajj information between supported languages."""
    engine = _get_engine()
    try:
        result = engine.translate(
            body.text,
            body.target_language.value,
            body.source_language.value,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI provider error: {str(e)}",
        )

    return TranslateResponse(
        original=body.text,
        translated=result.text,
        source_language=body.source_language.value,
        target_language=body.target_language.value,
        model_used=result.model,
    )


@router.post("/process", response_model=ProcessResponse)
def process_announcement(
    body: ProcessRequest,
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    """Full pipeline: simplify + translate → structured JSON output."""
    engine = _get_engine()
    try:
        result = engine.process(
            body.text,
            body.target_language.value,
            body.audio_required,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI provider error: {str(e)}",
        )

    return ProcessResponse(**result)


class HealthCheckResponse(BaseModel):
    provider: str
    configured: bool


@router.get("/health", response_model=HealthCheckResponse)
def ai_health(
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    """Check if the AI provider is configured."""
    api_key = os.environ.get("GEMINI_API_KEY", "")
    return HealthCheckResponse(
        provider="gemini",
        configured=bool(api_key),
    )
