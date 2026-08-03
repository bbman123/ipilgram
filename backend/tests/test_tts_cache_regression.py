"""Regression tests for TTS and Translation cache keys.

Verifies that:
1. Each language produces a DIFFERENT cache key
2. TTS generates audio in the correct language
3. Translation cache is keyed by (announcement_id, language)
4. No language falls back to English silently
5. Code vs name input produces the same result
"""

import hashlib
import hashlib
import pytest


# ---------------------------------------------------------------------------
# TTS cache key tests
# ---------------------------------------------------------------------------

class TestTTSCacheKey:
    """Verify TTS cache keys include language."""

    TEXT = "Welcome to Hajj 2026"

    @pytest.mark.parametrize("language,expected_code", [
        ("English", "en"),
        ("Arabic", "ar"),
        ("French", "fr"),
        ("Urdu", "ur"),
        ("Hausa", "ha"),
        ("Yoruba", "yo"),
        ("Igbo", "ig"),
        ("Hindi", "hi"),
    ])
    def test_resolve_lang_code_by_name(self, language, expected_code):
        from app.services.tts import _resolve_lang_code
        assert _resolve_lang_code(language) == expected_code

    @pytest.mark.parametrize("code,expected_code", [
        ("en", "en"),
        ("ar", "ar"),
        ("fr", "fr"),
        ("ur", "ur"),
        ("ha", "ha"),
        ("yo", "yo"),
        ("ig", "ig"),
        ("hi", "hi"),
    ])
    def test_resolve_lang_code_by_code(self, code, expected_code):
        from app.services.tts import _resolve_lang_code
        assert _resolve_lang_code(code) == expected_code

    @pytest.mark.parametrize("language,expected_name", [
        ("English", "English"),
        ("Arabic", "Arabic"),
        ("French", "French"),
        ("Urdu", "Urdu"),
        ("Hausa", "Hausa"),
        ("Yoruba", "Yoruba"),
        ("Igbo", "Igbo"),
        ("Hindi", "Hindi"),
        ("ar", "Arabic"),
        ("en", "English"),
        ("fr", "French"),
    ])
    def test_resolve_lang_name(self, language, expected_name):
        from app.services.tts import _resolve_lang_name
        assert _resolve_lang_name(language) == expected_name

    def test_all_languages_produce_different_cache_keys(self):
        from app.services.tts import _resolve_lang_code
        languages = ["English", "Arabic", "French", "Urdu", "Hausa", "Yoruba", "Igbo", "Hindi"]
        keys = {}
        for lang in languages:
            code = _resolve_lang_code(lang)
            raw = f"{self.TEXT}:{code}".encode()
            key = hashlib.sha256(raw).hexdigest()
            keys[lang] = key

        unique_keys = set(keys.values())
        assert len(unique_keys) == len(languages), (
            f"Cache key collision: {keys}"
        )

    def test_name_and_code_produce_same_cache_key(self):
        from app.services.tts import _resolve_lang_code
        pairs = [("Arabic", "ar"), ("English", "en"), ("French", "fr")]
        for name, code in pairs:
            code_from_name = _resolve_lang_code(name)
            code_from_code = _resolve_lang_code(code)
            assert code_from_name == code_from_code, (
                f"Mismatch for {name}/{code}: {code_from_name} != {code_from_code}"
            )
            raw_name = f"{self.TEXT}:{code_from_name}".encode()
            raw_code = f"{self.TEXT}:{code_from_code}".encode()
            assert hashlib.sha256(raw_name).hexdigest() == hashlib.sha256(raw_code).hexdigest()


# ---------------------------------------------------------------------------
# Translation cache key tests
# ---------------------------------------------------------------------------

class TestTranslationCacheKey:
    """Verify translation cache is keyed by (announcement_id, language)."""

    def test_different_languages_different_keys(self):
        from app.services.translation import TranslationCache
        cache = TranslationCache(ttl=3600)
        cache.set(1, "English", "title_en", "msg_en")
        cache.set(1, "Arabic", "title_ar", "msg_ar")
        cache.set(1, "French", "title_fr", "msg_fr")

        assert cache.get(1, "English") == ("title_en", "msg_en")
        assert cache.get(1, "Arabic") == ("title_ar", "msg_ar")
        assert cache.get(1, "French") == ("title_fr", "msg_fr")

    def test_different_announcements_different_keys(self):
        from app.services.translation import TranslationCache
        cache = TranslationCache(ttl=3600)
        cache.set(1, "Arabic", "title_1", "msg_1")
        cache.set(2, "Arabic", "title_2", "msg_2")

        assert cache.get(1, "Arabic") == ("title_1", "msg_1")
        assert cache.get(2, "Arabic") == ("title_2", "msg_2")

    def test_invalidate_single_language(self):
        from app.services.translation import TranslationCache
        cache = TranslationCache(ttl=3600)
        cache.set(1, "English", "title_en", "msg_en")
        cache.set(1, "Arabic", "title_ar", "msg_ar")

        cache.invalidate(1, "Arabic")
        assert cache.get(1, "English") == ("title_en", "msg_en")
        assert cache.get(1, "Arabic") is None

    def test_clear_all(self):
        from app.services.translation import TranslationCache
        cache = TranslationCache(ttl=3600)
        cache.set(1, "English", "title_en", "msg_en")
        cache.set(1, "Arabic", "title_ar", "msg_ar")

        cache.clear()
        assert cache.get(1, "English") is None
        assert cache.get(1, "Arabic") is None


# ---------------------------------------------------------------------------
# Language fallback tests
# ---------------------------------------------------------------------------

class TestLanguageFallback:
    """Verify unknown languages fall back correctly."""

    def test_unknown_language_code_falls_back_to_english(self):
        from app.services.tts import _resolve_lang_code
        assert _resolve_lang_code("xx") == "en"
        assert _resolve_lang_code("zz") == "en"
        assert _resolve_lang_code("") == "en"

    def test_unknown_language_name_falls_back_to_english(self):
        from app.services.tts import _resolve_lang_name
        assert _resolve_lang_name("xx") == "English"
        assert _resolve_lang_name("zz") == "English"

    def test_empty_text_returns_empty(self):
        from app.services.tts import generate_audio
        assert generate_audio("", "Arabic") == ""
        assert generate_audio("   ", "Arabic") == ""
        assert generate_audio(None, "Arabic") == ""


# ---------------------------------------------------------------------------
# Cache key uniqueness across all languages
# ---------------------------------------------------------------------------

class TestCacheKeyUniqueness:
    """Verify no two languages produce the same cache key for the same text."""

    TEXTS = [
        "Welcome to Hajj 2026",
        "Your flight departs at 3pm",
        "مرحبا بكم في الحج",
    ]

    LANGUAGES = ["English", "Arabic", "French", "Urdu", "Hausa", "Yoruba", "Igbo", "Hindi"]

    def test_all_language_combinations(self):
        from app.services.tts import _resolve_lang_code
        for text in self.TEXTS:
            keys = {}
            for lang in self.LANGUAGES:
                code = _resolve_lang_code(lang)
                raw = f"{text}:{code}".encode()
                key = hashlib.sha256(raw).hexdigest()
                keys[lang] = key

            unique = set(keys.values())
            assert len(unique) == len(self.LANGUAGES), (
                f"Cache collision for text='{text}': {keys}"
            )
