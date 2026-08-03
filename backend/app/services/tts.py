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
    "French": "fr",
    "Urdu": "ur",
    "Hindi": "hi",
}

# Reverse lookup: code → name (for callers that pass language codes)
_CODE_TO_NAME = {v: k for k, v in LANGUAGE_MAP.items()}

FALLBACK_LANGUAGE = "en"


def _resolve_lang_code(language: str) -> str:
    """Resolve a language name or code to a gTTS language code.

    Accepts both names ("Arabic") and codes ("ar").
    Returns the 2-letter gTTS code.
    """
    if language in LANGUAGE_MAP:
        return LANGUAGE_MAP[language]
    if language in _CODE_TO_NAME:
        return language
    return FALLBACK_LANGUAGE


def _resolve_lang_name(language: str) -> str:
    """Resolve a language name or code to a canonical language name.

    Accepts both names ("Arabic") and codes ("ar").
    Returns the display name ("Arabic").
    """
    if language in LANGUAGE_MAP:
        return language
    if language in _CODE_TO_NAME:
        return _CODE_TO_NAME[language]
    return "English"


def _cache_key(text: str, lang_code: str) -> str:
    raw = f"{text}:{lang_code}".encode()
    return hashlib.sha256(raw).hexdigest()


def generate_audio(text: str, language: str) -> str:
    """Generate audio file from text and language.

    Accepts both language names ("Arabic") and codes ("ar").
    Returns the relative URL path to the cached audio file.
    Caches by SHA-256(text + language_code).
    Falls back to English if the requested language is not supported.
    """
    if not text or not text.strip():
        logger.warning("generate_audio called with empty text")
        return ""

    lang_name = _resolve_lang_name(language)
    lang_code = _resolve_lang_code(language)
    key = _cache_key(text, lang_code)
    filename = f"{key}.mp3"
    filepath = AUDIO_CACHE_DIR / filename

    if filepath.exists():
        size = filepath.stat().st_size
        logger.info(
            "TTS cache hit: language=%s, code=%s, file=%s, size=%d bytes",
            lang_name, lang_code, filename, size,
        )
        if size == 0:
            logger.warning("TTS cache is 0 bytes, regenerating: %s", filename)
            filepath.unlink()
        else:
            return f"/api/v1/tts/audio/{filename}"

    try:
        logger.info("TTS generating: language=%s, code=%s, text_length=%d", lang_name, lang_code, len(text))
        tts = gTTS(text=text, lang=lang_code)
        tts.save(str(filepath))
        size = filepath.stat().st_size
        logger.info(
            "TTS generated: language=%s, code=%s, file=%s, size=%d bytes",
            lang_name, lang_code, filename, size,
        )
        return f"/api/v1/tts/audio/{filename}"
    except Exception as e:
        logger.error("TTS generation failed: language=%s, code=%s, error=%s", lang_name, lang_code, str(e))
        if lang_code != FALLBACK_LANGUAGE:
            try:
                logger.info("TTS fallback to English: text_length=%d", len(text))
                fallback_key = _cache_key(text, FALLBACK_LANGUAGE)
                fallback_filename = f"{fallback_key}.mp3"
                fallback_filepath = AUDIO_CACHE_DIR / fallback_filename

                if fallback_filepath.exists() and fallback_filepath.stat().st_size > 0:
                    logger.info("TTS fallback cache hit: file=%s", fallback_filename)
                    return f"/api/v1/tts/audio/{fallback_filename}"

                tts = gTTS(text=text, lang=FALLBACK_LANGUAGE)
                tts.save(str(fallback_filepath))
                logger.info("TTS fallback generated: file=%s, size=%d bytes", fallback_filename, fallback_filepath.stat().st_size)
                return f"/api/v1/tts/audio/{fallback_filename}"
            except Exception as fallback_error:
                logger.error("TTS fallback also failed: %s", str(fallback_error))
        raise
