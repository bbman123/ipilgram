"""Translation service using Gemini AI with in-memory caching.

Announcements are stored in English (canonical). This service translates
title and message to the user's preferred language on-the-fly, caching
results to avoid repeated AI calls for the same content + language pair.
"""

import hashlib
import logging
import time
import threading

from app.core.config import get_settings
from app.services.ai.gemini import GeminiProvider, GeminiError

logger = logging.getLogger("hajj_api")

# ---------------------------------------------------------------------------
# In-memory translation cache with TTL
# ---------------------------------------------------------------------------

_TRANSLATION_TTL_SECONDS = 3600  # 1 hour


class _TranslationCache:
    """Thread-safe in-memory cache for translations.

    Key: SHA-256(source_text + target_language)
    Value: (translated_text, timestamp)
    """

    def __init__(self, ttl: int = _TRANSLATION_TTL_SECONDS):
        self._store: dict[str, tuple[str, float]] = {}
        self._lock = threading.Lock()
        self._ttl = ttl

    @staticmethod
    def _key(text: str, language: str) -> str:
        raw = f"{text}:{language}".encode()
        return hashlib.sha256(raw).hexdigest()

    def get(self, text: str, language: str) -> str | None:
        key = self._key(text, language)
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            translated, ts = entry
            if time.time() - ts > self._ttl:
                del self._store[key]
                return None
            return translated

    def set(self, text: str, language: str, translated: str) -> None:
        key = self._key(text, language)
        with self._lock:
            self._store[key] = (translated, time.time())

    def invalidate(self, text: str, language: str) -> None:
        key = self._key(text, language)
        with self._lock:
            self._store.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._store)


_cache = _TranslationCache()

# ---------------------------------------------------------------------------
# Supported languages
# ---------------------------------------------------------------------------

SUPPORTED_LANGUAGES = {
    "English": "en",
    "Hausa": "ha",
    "Yoruba": "yo",
    "Igbo": "ig",
    "Arabic": "ar",
}


def _get_provider() -> GeminiProvider | None:
    settings = get_settings()
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return None
    return GeminiProvider(api_key)


# ---------------------------------------------------------------------------
# Core translation
# ---------------------------------------------------------------------------

_TRANSLATION_SYSTEM_INSTRUCTION = """You are a professional translator for Hajj pilgrimage information.

RULES:
- Translate the given text into the target language.
- Preserve all proper nouns (flight numbers, hotel names, place names, times, dates).
- Keep numbers and times unchanged.
- Use natural, clear phrasing that anyone can understand.
- Do NOT add explanations, notes, or commentary.
- Return ONLY the translated text, nothing else.
- If the target language is English, return the original text unchanged.
- Preserve any {{placeholder}} patterns exactly as they appear."""


def translate_text(text: str, target_language: str) -> str:
    """Translate text to the target language using Gemini.

    Returns cached result if available. Falls back to original text on failure.
    """
    if not text or not text.strip():
        return text

    if target_language == "English":
        return text

    cached = _cache.get(text, target_language)
    if cached is not None:
        logger.debug("Translation cache hit: language=%s, length=%d", target_language, len(cached))
        return cached

    provider = _get_provider()
    if provider is None:
        logger.warning("Translation skipped: Gemini not configured")
        return text

    prompt = f"""Translate the following text to {target_language}.

Text to translate:
{text}

Return ONLY the translated text."""

    try:
        logger.info("Translating to %s, input_length=%d", target_language, len(text))
        ai_response = provider.generate(prompt, _TRANSLATION_SYSTEM_INSTRUCTION)
        translated = ai_response.text.strip()

        if not translated:
            logger.warning("Gemini returned empty translation, falling back to original")
            return text

        _cache.set(text, target_language, translated)
        logger.info(
            "Translation complete: language=%s, input_length=%d, output_length=%d",
            target_language,
            len(text),
            len(translated),
        )
        return translated

    except GeminiError as e:
        logger.error("Gemini translation error: %s (reason=%s)", e.message, e.details)
        return text
    except Exception as e:
        logger.error("Unexpected translation error: %s", str(e))
        return text


def translate_pair(
    title: str,
    message: str,
    target_language: str,
) -> tuple[str, str]:
    """Translate both title and message to the target language.

    Returns (translated_title, translated_message).
    Falls back to originals on failure.
    """
    if target_language == "English":
        return title, message

    translated_title = translate_text(title, target_language)
    translated_message = translate_text(message, target_language)
    return translated_title, translated_message


def get_cache_stats() -> dict:
    """Return translation cache statistics."""
    return {
        "cache_size": _cache.size,
        "ttl_seconds": _cache._ttl,
    }


def clear_cache() -> None:
    """Clear the translation cache."""
    _cache.clear()
    logger.info("Translation cache cleared")
