"""Translation service using Gemini AI with announcement-level caching.

Announcements are stored in English (canonical). This service translates
title and message to the user's preferred language on-the-fly, caching
by AnnouncementID + Language to avoid repeated AI calls.
"""

import logging
import time
import threading
from typing import NamedTuple

from app.core.config import get_settings
from app.services.ai.gemini import GeminiProvider, GeminiError

logger = logging.getLogger("hajj_api")

# ---------------------------------------------------------------------------
# Supported languages
# ---------------------------------------------------------------------------

SUPPORTED_LANGUAGES: dict[str, str] = {
    "English": "en",
    "Hausa": "ha",
    "Yoruba": "yo",
    "Igbo": "ig",
    "Arabic": "ar",
    "French": "fr",
    "Urdu": "ur",
    "Hindi": "hi",
}

# ---------------------------------------------------------------------------
# Translation cache (keyed by announcement_id + language)
# ---------------------------------------------------------------------------

_TRANSLATION_TTL_SECONDS = 3600  # 1 hour


class _CacheEntry(NamedTuple):
    title: str
    message: str
    timestamp: float


class TranslationCache:
    """Thread-safe in-memory cache for announcement translations.

    Key: (announcement_id, language)
    Value: (_CacheEntry)
    """

    def __init__(self, ttl: int = _TRANSLATION_TTL_SECONDS):
        self._store: dict[tuple[int, str], _CacheEntry] = {}
        self._lock = threading.Lock()
        self._ttl = ttl

    def get(self, announcement_id: int, language: str) -> tuple[str, str] | None:
        key = (announcement_id, language)
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            if time.time() - entry.timestamp > self._ttl:
                del self._store[key]
                return None
            return entry.title, entry.message

    def set(self, announcement_id: int, language: str, title: str, message: str) -> None:
        key = (announcement_id, language)
        with self._lock:
            self._store[key] = _CacheEntry(
                title=title,
                message=message,
                timestamp=time.time(),
            )

    def has(self, announcement_id: int, language: str) -> bool:
        key = (announcement_id, language)
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return False
            if time.time() - entry.timestamp > self._ttl:
                del self._store[key]
                return False
            return True

    def invalidate(self, announcement_id: int, language: str) -> None:
        key = (announcement_id, language)
        with self._lock:
            self._store.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._store)


# ---------------------------------------------------------------------------
# TranslationService
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


class TranslationService:
    """Translates announcements using Gemini AI with caching.

    Usage:
        service = TranslationService()
        title, message = service.translate_announcement(
            announcement_id=4,
            title="Flight Update",
            message="Your flight departs at 8:00 AM",
            target_language="Arabic",
        )
    """

    def __init__(self):
        self.cache = TranslationCache()
        self._provider: GeminiProvider | None = None

    def _get_provider(self) -> GeminiProvider | None:
        if self._provider is not None:
            return self._provider
        settings = get_settings()
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            return None
        self._provider = GeminiProvider(api_key)
        return self._provider

    def translate_text(self, text: str, target_language: str) -> tuple[str, bool]:
        """Translate a single text string to the target language.

        Returns (translated_text, was_translated).
        On failure, returns (original_text, False) — never silently returns English as translated.
        """
        if not text or not text.strip():
            return text, False

        if target_language == "English":
            return text, False

        provider = self._get_provider()
        if provider is None:
            logger.warning("Translation SKIPPED: Gemini not configured, falling back to English")
            return text, False

        prompt = f"""Translate the following text to {target_language}.

Text to translate:
{text}

Return ONLY the translated text."""

        try:
            logger.info("Translating to %s, input_length=%d", target_language, len(text))
            ai_response = provider.generate(prompt, _TRANSLATION_SYSTEM_INSTRUCTION)
            translated = ai_response.text.strip()

            if not translated:
                logger.warning("Gemini returned empty translation, falling back to English")
                return text, False

            logger.info(
                "Translation complete: language=%s, input_length=%d, output_length=%d, tokens=%d",
                target_language,
                len(text),
                len(translated),
                ai_response.tokens_used,
            )
            return translated, True

        except GeminiError as e:
            logger.error("Gemini translation FAILED: %s (reason=%s) — falling back to English", e.message, e.details)
            return text, False
        except Exception as e:
            logger.error("Unexpected translation FAILED: %s — falling back to English", str(e))
            return text, False

    def translate_announcement(
        self,
        announcement_id: int,
        title: str,
        message: str,
        target_language: str,
    ) -> tuple[str, str, bool]:
        """Translate an announcement's title and message.

        Returns (translated_title, translated_message, was_translated).
        Caches by announcement_id + language.
        Only caches when translation actually succeeded.
        """
        if target_language == "English":
            return title, message, False

        cached = self.cache.get(announcement_id, target_language)
        if cached is not None:
            logger.info("Translation cache hit: announcement_id=%d, language=%s, title_len=%d, msg_len=%d",
                        announcement_id, target_language, len(cached[0]), len(cached[1]))
            return cached[0], cached[1], True

        translated_title, title_ok = self.translate_text(title, target_language)
        translated_message, message_ok = self.translate_text(message, target_language)

        was_translated = title_ok or message_ok

        if was_translated:
            self.cache.set(announcement_id, target_language, translated_title, translated_message)
            logger.info(
                "Announcement %d translated to %s — CACHED: title_len=%d, msg_len=%d",
                announcement_id,
                target_language,
                len(translated_title),
                len(translated_message),
            )
        else:
            logger.warning(
                "Announcement %d translation to %s FAILED — returning English, NOT caching",
                announcement_id,
                target_language,
            )

        return translated_title, translated_message, was_translated

    def get_cache_stats(self) -> dict:
        """Return cache statistics."""
        return {
            "cache_size": self.cache.size,
            "ttl_seconds": self.cache._ttl,
        }

    def clear_cache(self) -> None:
        """Clear the translation cache."""
        self.cache.clear()
        logger.info("Translation cache cleared")


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

translation_service = TranslationService()
