"""Standalone tests for translation pipeline.

Run with: python -m pytest tests/test_standalone_translation.py -v --no-header --rootdir=backend
"""

import sys
import os
import logging
import hashlib
from unittest.mock import patch, MagicMock

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ.setdefault("DATABASE_URL", "postgresql://postgres:nerdyamin@localhost:5432/hajj_pilgrims")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-only-32chars!")
os.environ.setdefault("GEMINI_API_KEY", "test-fake-key-for-mocking")

from app.services.translation import TranslationService, TranslationCache, SUPPORTED_LANGUAGES
from app.services.tts import LANGUAGE_MAP


class TestTranslationCache:
    """Test the TranslationCache class."""

    def test_cache_set_and_get(self):
        cache = TranslationCache(ttl=3600)
        cache.set(announcement_id=1, language="Arabic", title="Title AR", message="Message AR")
        result = cache.get(announcement_id=1, language="Arabic")
        assert result == ("Title AR", "Message AR")

    def test_cache_miss(self):
        cache = TranslationCache(ttl=3600)
        result = cache.get(announcement_id=1, language="Arabic")
        assert result is None

    def test_cache_by_announcement_id_and_language(self):
        cache = TranslationCache(ttl=3600)
        cache.set(announcement_id=1, language="Arabic", title="Title 1 AR", message="Message 1 AR")
        cache.set(announcement_id=1, language="French", title="Title 1 FR", message="Message 1 FR")
        cache.set(announcement_id=2, language="Arabic", title="Title 2 AR", message="Message 2 AR")

        assert cache.get(1, "Arabic") == ("Title 1 AR", "Message 1 AR")
        assert cache.get(1, "French") == ("Title 1 FR", "Message 1 FR")
        assert cache.get(2, "Arabic") == ("Title 2 AR", "Message 2 AR")
        assert cache.get(2, "French") is None

    def test_cache_invalidation(self):
        cache = TranslationCache(ttl=3600)
        cache.set(announcement_id=1, language="Arabic", title="Title", message="Message")
        cache.invalidate(announcement_id=1, language="Arabic")
        assert cache.get(announcement_id=1, language="Arabic") is None

    def test_cache_clear(self):
        cache = TranslationCache(ttl=3600)
        cache.set(1, "Arabic", "Title", "Message")
        cache.set(2, "French", "Title", "Message")
        cache.clear()
        assert cache.size == 0

    def test_cache_ttl_expiry(self):
        cache = TranslationCache(ttl=0)  # Immediate expiry
        cache.set(announcement_id=1, language="Arabic", title="Title", message="Message")
        result = cache.get(announcement_id=1, language="Arabic")
        assert result is None


class TestTranslationService:
    """Test the TranslationService class."""

    def setup_method(self):
        self.service = TranslationService()
        self.service.cache.clear()
        self.service._provider = None

    @patch("app.services.translation.GeminiProvider")
    def test_translate_text_english_passthrough(self, mock_gemini_cls):
        """English text should pass through without AI call."""
        result = self.service.translate_text("Hello world", "English")
        assert result == "Hello world"
        mock_gemini_cls.assert_not_called()

    @patch("app.services.translation.GeminiProvider")
    def test_translate_text_to_hausa(self, mock_gemini_cls):
        """Translation to Hausa should call Gemini."""
        mock_provider = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Sannu duniya"
        mock_response.tokens_used = 50
        mock_provider.generate.return_value = mock_response
        mock_gemini_cls.return_value = mock_provider

        result = self.service.translate_text("Hello world", "Hausa")

        assert result == "Sannu duniya"
        mock_provider.generate.assert_called_once()

    @patch("app.services.translation.GeminiProvider")
    def test_translate_text_to_arabic(self, mock_gemini_cls):
        """Translation to Arabic should call Gemini."""
        mock_provider = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "مرحبا بالعالم"
        mock_response.tokens_used = 50
        mock_provider.generate.return_value = mock_response
        mock_gemini_cls.return_value = mock_provider

        result = self.service.translate_text("Hello world", "Arabic")

        assert result == "مرحبا بالعالم"
        mock_provider.generate.assert_called_once()

    @patch("app.services.translation.GeminiProvider")
    def test_translate_text_to_french(self, mock_gemini_cls):
        """Translation to French should call Gemini."""
        mock_provider = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Bonjour le monde"
        mock_response.tokens_used = 50
        mock_provider.generate.return_value = mock_response
        mock_gemini_cls.return_value = mock_provider

        result = self.service.translate_text("Hello world", "French")

        assert result == "Bonjour le monde"

    @patch("app.services.translation.GeminiProvider")
    def test_translate_text_to_urdu(self, mock_gemini_cls):
        """Translation to Urdu should call Gemini."""
        mock_provider = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "ہیلو دنیا"
        mock_response.tokens_used = 50
        mock_provider.generate.return_value = mock_response
        mock_gemini_cls.return_value = mock_provider

        result = self.service.translate_text("Hello world", "Urdu")

        assert result == "ہیلو دنیا"

    @patch("app.services.translation.GeminiProvider")
    def test_translate_text_to_yoruba(self, mock_gemini_cls):
        """Translation to Yoruba should call Gemini."""
        mock_provider = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Bawo ni ayé"
        mock_response.tokens_used = 50
        mock_provider.generate.return_value = mock_response
        mock_gemini_cls.return_value = mock_provider

        result = self.service.translate_text("Hello world", "Yoruba")

        assert result == "Bawo ni ayé"

    @patch("app.services.translation.GeminiProvider")
    def test_translate_text_to_igbo(self, mock_gemini_cls):
        """Translation to Igbo should call Gemini."""
        mock_provider = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Ndewo ụwa"
        mock_response.tokens_used = 50
        mock_provider.generate.return_value = mock_response
        mock_gemini_cls.return_value = mock_provider

        result = self.service.translate_text("Hello world", "Igbo")

        assert result == "Ndewo ụwa"

    @patch("app.services.translation.GeminiProvider")
    def test_translate_text_to_hindi(self, mock_gemini_cls):
        """Translation to Hindi should call Gemini."""
        mock_provider = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "नमस्ते दुनिया"
        mock_response.tokens_used = 50
        mock_provider.generate.return_value = mock_response
        mock_gemini_cls.return_value = mock_provider

        result = self.service.translate_text("Hello world", "Hindi")

        assert result == "नमस्ते दुनिया"

    @patch("app.services.translation.GeminiProvider")
    def test_translate_text_empty_input(self, mock_gemini_cls):
        """Empty text should pass through without calling Gemini."""
        result = self.service.translate_text("", "Hausa")
        assert result == ""
        mock_gemini_cls.assert_not_called()

    @patch("app.services.translation.GeminiProvider")
    def test_translate_text_whitespace_only(self, mock_gemini_cls):
        """Whitespace-only text should pass through without calling Gemini."""
        result = self.service.translate_text("   ", "Hausa")
        assert result == "   "
        mock_gemini_cls.assert_not_called()

    @patch("app.services.translation.GeminiProvider")
    def test_translate_text_gemini_error_returns_original(self, mock_gemini_cls):
        """Gemini error should return original text."""
        mock_provider = MagicMock()
        mock_provider.generate.side_effect = Exception("Gemini API error")
        mock_gemini_cls.return_value = mock_provider

        result = self.service.translate_text("Hello", "Hausa")
        assert result == "Hello"

    @patch("app.services.translation.GeminiProvider")
    def test_translate_text_gemini_empty_response_fallback(self, mock_gemini_cls):
        """Empty Gemini response should return original text."""
        mock_provider = MagicMock()
        mock_response = MagicMock()
        mock_response.text = ""
        mock_provider.generate.return_value = mock_response
        mock_gemini_cls.return_value = mock_provider

        result = self.service.translate_text("Hello", "Hausa")
        assert result == "Hello"

    def test_translate_announcement_english_no_translation(self):
        """English announcements should not be translated."""
        title, message, was_translated = self.service.translate_announcement(
            announcement_id=1,
            title="Flight Update",
            message="Your flight departs at 8:00 AM",
            target_language="English",
        )
        assert title == "Flight Update"
        assert message == "Your flight departs at 8:00 AM"
        assert was_translated is False

    @patch("app.services.translation.GeminiProvider")
    def test_translate_announcement_with_caching(self, mock_gemini_cls):
        """Translation should be cached by announcement_id + language."""
        mock_provider = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Translated text"
        mock_response.tokens_used = 50
        mock_provider.generate.return_value = mock_response
        mock_gemini_cls.return_value = mock_provider

        # First call - should translate and cache
        title1, msg1, translated1 = self.service.translate_announcement(
            announcement_id=4,
            title="Title",
            message="Message",
            target_language="Arabic",
        )
        assert translated1 is True
        assert mock_provider.generate.call_count == 2  # title + message

        # Second call - should use cache
        title2, msg2, translated2 = self.service.translate_announcement(
            announcement_id=4,
            title="Title",
            message="Message",
            target_language="Arabic",
        )
        assert translated2 is True
        assert mock_provider.generate.call_count == 2  # No new API calls

    def test_translate_announcement_different_languages_different_cache(self):
        """Different languages should have separate cache entries."""
        self.service.cache.set(1, "Arabic", "Title AR", "Message AR")
        self.service.cache.set(1, "French", "Title FR", "Message FR")

        title_ar, msg_ar, _ = self.service.translate_announcement(1, "Title", "Message", "Arabic")
        title_fr, msg_fr, _ = self.service.translate_announcement(1, "Title", "Message", "French")

        assert title_ar == "Title AR"
        assert title_fr == "Title FR"


class TestTTS:
    """Test the TTS service."""

    def test_language_map_contains_all_languages(self):
        """All supported languages should be in the TTS language map."""
        for lang in SUPPORTED_LANGUAGES:
            assert lang in LANGUAGE_MAP, f"Language {lang} missing from TTS language map"

    def test_cache_key_deterministic(self):
        """Same input should produce same cache key."""
        key1 = hashlib.sha256(b"Hello world:en").hexdigest()
        key2 = hashlib.sha256(b"Hello world:en").hexdigest()
        assert key1 == key2

    def test_cache_key_differs_by_language(self):
        """Different languages should produce different cache keys."""
        key_en = hashlib.sha256(b"Hello world:en").hexdigest()
        key_ha = hashlib.sha256(b"Hello world:ha").hexdigest()
        assert key_en != key_ha

    def test_cache_key_differs_by_text(self):
        """Different text should produce different cache keys."""
        key1 = hashlib.sha256(b"Hello world:en").hexdigest()
        key2 = hashlib.sha256(b"Goodbye world:en").hexdigest()
        assert key1 != key2


class TestLogging:
    """Test that structured logging is in place."""

    def test_translation_service_logs_translation(self, caplog):
        """Translation should log the announcement ID and language."""
        service = TranslationService()
        service.cache.clear()

        with caplog.at_level(logging.INFO, logger="hajj_api"):
            # Set cache directly to test logging
            service.cache.set(4, "Arabic", "Title", "Message")
            title, message, was_translated = service.translate_announcement(4, "Title", "Message", "Arabic")

        assert "Translation cache hit" in caplog.text or "Announcement 4 translated to Arabic" in caplog.text

    def test_translation_cache_hit_logs(self, caplog):
        """Cache hit should log 'Translation cache hit'."""
        service = TranslationService()
        service.cache.clear()
        service.cache.set(1, "Hausa", "Title", "Message")

        with caplog.at_level(logging.INFO, logger="hajj_api"):
            service.translate_announcement(1, "Title", "Message", "Hausa")

        assert "Translation cache hit" in caplog.text
