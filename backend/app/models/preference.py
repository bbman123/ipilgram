import enum
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class PreferredLanguage(str, enum.Enum):
    English = "English"
    Hausa = "Hausa"
    Yoruba = "Yoruba"
    Igbo = "Igbo"
    Arabic = "Arabic"


class DeliveryMode(str, enum.Enum):
    Text = "Text"
    Audio = "Audio"
    TextPlusAudio = "Text + Audio"


# Canonical mapping: display labels -> canonical enum values
DELIVERY_MODE_CANONICAL = {
    "Text": DeliveryMode.Text,
    "Audio": DeliveryMode.Audio,
    "Text + Audio": DeliveryMode.TextPlusAudio,
    "TextPlusAudio": DeliveryMode.TextPlusAudio,
    "text": DeliveryMode.Text,
    "audio": DeliveryMode.Audio,
    "text + audio": DeliveryMode.TextPlusAudio,
    "textplusaudio": DeliveryMode.TextPlusAudio,
    "text_and_audio": DeliveryMode.TextPlusAudio,
    "text + audio": DeliveryMode.TextPlusAudio,
}


class DeliveryModeType(sa.types.TypeDecorator):
    """Custom SQLAlchemy type that handles both enum names and values.

    SQLAlchemy's Enum type uses member NAMES for deserialization by default.
    When the DB contains "Text + Audio" (the value), SQLAlchemy looks for a
    member named "Text + Audio" but finds "TextPlusAudio" instead.

    This adapter normalizes the input before deserialization.
    """

    impl = sa.Enum
    cache_ok = True

    def __init__(self):
        self.impl = sa.Enum(
            "Text",
            "Audio",
            "Text + Audio",
            name="deliverymode",
            create_type=False,
        )

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, str):
            return DeliveryMode(value)
        return value


class Preference(Base):
    __tablename__ = "preferences"

    id: Mapped[int] = mapped_column(primary_key=True)
    pilgrim_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    preferred_language: Mapped[PreferredLanguage] = mapped_column(
        sa.Enum(PreferredLanguage, name="preferredlanguage", create_type=False),
        default=PreferredLanguage.English,
    )
    delivery_mode: Mapped[DeliveryMode] = mapped_column(
        DeliveryModeType(),
        default=DeliveryMode.Text,
    )
    font_size: Mapped[int] = mapped_column(Integer, default=16)
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
