"""Tests for DeliveryMode normalization across the stack."""
import pytest
from app.models.preference import (
    DeliveryMode,
    DeliveryModeType,
    DELIVERY_MODE_CANONICAL,
)
from app.schemas.preference import PreferenceCreate, PreferenceUpdate


# ─── Backend enum tests ─────────────────────────────────────────────


class TestDeliveryModeEnum:
    def test_canonical_values(self):
        assert DeliveryMode.Text.value == "Text"
        assert DeliveryMode.Audio.value == "Audio"
        assert DeliveryMode.TextPlusAudio.value == "Text + Audio"

    def test_canonical_names(self):
        assert DeliveryMode.Text.name == "Text"
        assert DeliveryMode.Audio.name == "Audio"
        assert DeliveryMode.TextPlusAudio.name == "TextPlusAudio"


class TestDeliveryModeCanonicalMap:
    def test_display_labels_map_to_canonical(self):
        assert DELIVERY_MODE_CANONICAL["Text"] == DeliveryMode.Text
        assert DELIVERY_MODE_CANONICAL["Audio"] == DeliveryMode.Audio
        assert DELIVERY_MODE_CANONICAL["Text + Audio"] == DeliveryMode.TextPlusAudio

    def test_canonical_values_map_to_themselves(self):
        assert DELIVERY_MODE_CANONICAL["Text"] == DeliveryMode.Text
        assert DELIVERY_MODE_CANONICAL["Audio"] == DeliveryMode.Audio
        assert DELIVERY_MODE_CANONICAL["TextPlusAudio"] == DeliveryMode.TextPlusAudio

    def test_case_insensitive(self):
        assert DELIVERY_MODE_CANONICAL["text"] == DeliveryMode.Text
        assert DELIVERY_MODE_CANONICAL["audio"] == DeliveryMode.Audio
        assert DELIVERY_MODE_CANONICAL["textplusaudio"] == DeliveryMode.TextPlusAudio


class TestDeliveryModeType:
    """Test the custom SQLAlchemy type adapter."""

    def test_result_value_is_canonical(self):
        impl = DeliveryModeType()
        result = impl.process_result_value("Text + Audio", None)
        assert result == DeliveryMode.TextPlusAudio

    def test_result_value_passthrough(self):
        impl = DeliveryModeType()
        result = impl.process_result_value("Text", None)
        assert result == DeliveryMode.Text

    def test_result_value_none(self):
        impl = DeliveryModeType()
        result = impl.process_result_value(None, None)
        assert result is None

    def test_result_value_enum_member(self):
        impl = DeliveryModeType()
        result = impl.process_result_value(DeliveryMode.TextPlusAudio, None)
        assert result == DeliveryMode.TextPlusAudio


# ─── Pydantic schema tests ─────────────────────────────────────────


class TestPreferenceCreateSchema:
    def test_legacy_delivery_mode_normalized(self):
        pref = PreferenceCreate(
            pilgrim_id=1,
            preferred_language="English",
            delivery_mode="Text + Audio",
        )
        assert pref.delivery_mode == DeliveryMode.TextPlusAudio

    def test_canonical_delivery_mode_preserved(self):
        pref = PreferenceCreate(
            pilgrim_id=1,
            preferred_language="English",
            delivery_mode="TextPlusAudio",
        )
        assert pref.delivery_mode == DeliveryMode.TextPlusAudio

    def test_audio_delivery_mode(self):
        pref = PreferenceCreate(
            pilgrim_id=1,
            preferred_language="English",
            delivery_mode="Audio",
        )
        assert pref.delivery_mode == DeliveryMode.Audio

    def test_text_delivery_mode(self):
        pref = PreferenceCreate(
            pilgrim_id=1,
            preferred_language="English",
            delivery_mode="Text",
        )
        assert pref.delivery_mode == DeliveryMode.Text


class TestPreferenceUpdateSchema:
    def test_legacy_delivery_mode_normalized(self):
        pref = PreferenceUpdate(delivery_mode="Text + Audio")
        assert pref.delivery_mode == DeliveryMode.TextPlusAudio

    def test_canonical_delivery_mode_preserved(self):
        pref = PreferenceUpdate(delivery_mode="TextPlusAudio")
        assert pref.delivery_mode == DeliveryMode.TextPlusAudio

    def test_audio_delivery_mode(self):
        pref = PreferenceUpdate(delivery_mode="Audio")
        assert pref.delivery_mode == DeliveryMode.Audio

    def test_none_delivery_mode(self):
        pref = PreferenceUpdate(delivery_mode=None)
        assert pref.delivery_mode is None
