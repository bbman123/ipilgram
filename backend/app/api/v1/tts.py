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
from app.services.tts import generate_audio, AUDIO_CACHE_DIR, _resolve_lang_code

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

    lang_code = _resolve_lang_code(body.language.value)
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


@router.api_route(
    "/audio/{filename}",
    methods=["GET", "HEAD"],
    summary="Download audio file",
    description="Serve a cached MP3 audio file by filename. No authentication required.",
    responses={
        200: {"description": "Audio file (audio/mpeg)"},
        404: {"description": "Audio file not found"},
    },
)
def serve_audio(filename: str):
    """Serve a cached audio file. No authentication required."""
    logger.info("[AUDIO_DIAG] serve_audio called: filename=%s", filename)

    safe_name = Path(filename).name
    if safe_name != filename or ".." in filename or "/" in filename or "\\" in filename:
        logger.warning("[AUDIO_DIAG] serve_audio rejected invalid filename: %s", filename)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found"
        )

    filepath = AUDIO_CACHE_DIR / safe_name
    file_exists = filepath.exists()
    is_mp3 = filepath.suffix == ".mp3" if file_exists else False
    file_size = filepath.stat().st_size if file_exists else 0

    logger.info(
        "[AUDIO_DIAG] serve_audio file check: filename=%s, file_exists=%s, is_mp3=%s, file_size=%d bytes, full_path=%s",
        safe_name, file_exists, is_mp3, file_size, str(filepath),
    )

    if not file_exists or not is_mp3:
        logger.warning("[AUDIO_DIAG] serve_audio returning 404: filename=%s, file_exists=%s, is_mp3=%s", safe_name, file_exists, is_mp3)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found"
        )

    logger.info("[AUDIO_DIAG] serve_audio returning file: filename=%s, content_type=audio/mpeg, file_size=%d bytes", safe_name, file_size)
    return FileResponse(str(filepath), media_type="audio/mpeg", filename=filename)
