import hashlib
import os
from pathlib import Path

from gtts import gTTS

AUDIO_CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "audio_cache"
AUDIO_CACHE_DIR.mkdir(exist_ok=True)

LANGUAGE_MAP = {
    "English": "en",
    "Hausa": "ha",
    "Yoruba": "yo",
    "Igbo": "ig",
    "Arabic": "ar",
}

FALLBACK_LANGUAGE = "en"


def _cache_key(text: str, lang_code: str) -> str:
    raw = f"{text}:{lang_code}".encode()
    return hashlib.sha256(raw).hexdigest()


def generate_audio(text: str, language: str) -> str:
    """Generate audio file from text and language.

    Returns the relative URL path to the cached audio file.
    Caches by SHA-256(text + language).
    """
    lang_code = LANGUAGE_MAP.get(language, FALLBACK_LANGUAGE)
    key = _cache_key(text, lang_code)
    filename = f"{key}.mp3"
    filepath = AUDIO_CACHE_DIR / filename

    if filepath.exists():
        return f"/api/v1/tts/audio/{filename}"

    tts = gTTS(text=text, lang=lang_code)
    tts.save(str(filepath))

    return f"/api/v1/tts/audio/{filename}"
