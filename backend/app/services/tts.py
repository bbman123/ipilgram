"""Text-to-Speech service using gTTS with file-based caching.

Generates MP3 audio files from text. Caches by SHA-256(text + language_code).
Falls back gracefully on errors — never crashes the caller.
"""

import hashlib
import logging
from pathlib import Path

from gtts import gTTS

logger = logging.getLogger("hajj_api")

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
    Falls back to English if the requested language is not supported.
    """
    if not text or not text.strip():
        logger.warning("generate_audio called with empty text")
        return ""

    lang_code = LANGUAGE_MAP.get(language, FALLBACK_LANGUAGE)
    key = _cache_key(text, lang_code)
    filename = f"{key}.mp3"
    filepath = AUDIO_CACHE_DIR / filename

    if filepath.exists():
        logger.debug("TTS cache hit: lang=%s, file=%s", language, filename)
        return f"/api/v1/tts/audio/{filename}"

    try:
        logger.info("Generating TTS: lang=%s, text_length=%d", language, len(text))
        tts = gTTS(text=text, lang=lang_code)
        tts.save(str(filepath))
        logger.info("TTS generated: lang=%s, file=%s, size=%d bytes", language, filename, filepath.stat().st_size)
        return f"/api/v1/tts/audio/{filename}"
    except Exception as e:
        logger.error("TTS generation failed: lang=%s, error=%s", language, str(e))
        # If the requested language failed, try English as fallback
        if lang_code != FALLBACK_LANGUAGE:
            try:
                logger.info("TTS fallback to English: text_length=%d", len(text))
                fallback_key = _cache_key(text, FALLBACK_LANGUAGE)
                fallback_filename = f"{fallback_key}.mp3"
                fallback_filepath = AUDIO_CACHE_DIR / fallback_filename

                if fallback_filepath.exists():
                    return f"/api/v1/tts/audio/{fallback_filename}"

                tts = gTTS(text=text, lang=FALLBACK_LANGUAGE)
                tts.save(str(fallback_filepath))
                logger.info("TTS fallback generated: file=%s", fallback_filename)
                return f"/api/v1/tts/audio/{fallback_filename}"
            except Exception as fallback_error:
                logger.error("TTS fallback also failed: %s", str(fallback_error))
        raise
