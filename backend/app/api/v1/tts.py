import hashlib
import logging
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import FileResponse

from app.api.deps import require_role
from app.core.rate_limit import limiter
from app.schemas.response import success_response
from app.models.user import User, Role
from app.schemas.tts import TTSRequest, TTSResponse
from app.services.tts import generate_audio, AUDIO_CACHE_DIR

logger = logging.getLogger("hajj_api")

router = APIRouter(prefix="/tts", tags=["Text-to-Speech"])


@router.post(
    "",
    summary="Convert text to speech",
    description="Generate an MP3 audio file from text. Supports English, Hausa, Yoruba, Igbo, and Arabic. Cached by text+language hash.",
    responses={
        200: {"description": "Audio URL and metadata returned"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        500: {"description": "TTS generation failed"},
    },
)
@limiter.limit("10/minute")
def text_to_speech(
    body: TTSRequest,
    request: Request,
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    try:
        audio_url = generate_audio(body.text, body.language.value)
    except Exception as e:
        logger.error("TTS generation error: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="TTS generation failed. Please try again later.",
        )

    lang_code = {"English": "en", "Hausa": "ha", "Yoruba": "yo", "Igbo": "ig", "Arabic": "ar"}.get(
        body.language.value, "en"
    )
    key = hashlib.sha256(f"{body.text}:{lang_code}".encode()).hexdigest()
    cached = (AUDIO_CACHE_DIR / f"{key}.mp3").exists()

    return success_response(
        data=TTSResponse(
            audio_url=audio_url,
            language=body.language.value,
            cached=cached,
        ).model_dump(),
        message="TTS generated successfully",
    )


@router.get(
    "/audio/{filename}",
    summary="Download audio file",
    description="Serve a cached MP3 audio file by filename. No authentication required.",
    responses={
        200: {"description": "Audio file (audio/mpeg)"},
        404: {"description": "Audio file not found"},
    },
)
def serve_audio(filename: str):
    """Serve a cached audio file. No authentication required."""
    safe_name = Path(filename).name
    if safe_name != filename or ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found"
        )

    filepath = AUDIO_CACHE_DIR / safe_name
    if not filepath.exists() or filepath.suffix != ".mp3":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found"
        )
    return FileResponse(str(filepath), media_type="audio/mpeg", filename=filename)
