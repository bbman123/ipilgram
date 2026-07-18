import hashlib
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from app.api.deps import require_role
from app.models.user import User, Role
from app.schemas.tts import TTSRequest, TTSResponse
from app.services.tts import generate_audio, AUDIO_CACHE_DIR

router = APIRouter(prefix="/tts", tags=["Text-to-Speech"])


@router.post("", response_model=TTSResponse)
def text_to_speech(
    body: TTSRequest,
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    """Convert text to speech audio file. Returns cached audio if available."""
    try:
        audio_url = generate_audio(body.text, body.language.value)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"TTS generation failed: {str(e)}",
        )

    lang_code = {"English": "en", "Hausa": "ha", "Yoruba": "yo", "Igbo": "ig", "Arabic": "ar"}.get(
        body.language.value, "en"
    )
    key = hashlib.sha256(f"{body.text}:{lang_code}".encode()).hexdigest()
    cached = (AUDIO_CACHE_DIR / f"{key}.mp3").exists()

    return TTSResponse(
        audio_url=audio_url,
        language=body.language.value,
        cached=cached,
    )


@router.get("/audio/{filename}")
def serve_audio(filename: str):
    """Serve a cached audio file."""
    filepath = AUDIO_CACHE_DIR / filename
    if not filepath.exists() or not filepath.suffix == ".mp3":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Audio not found"
        )
    return FileResponse(str(filepath), media_type="audio/mpeg", filename=filename)
