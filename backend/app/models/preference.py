import enum
from datetime import datetime

from sqlalchemy import String, Boolean, ForeignKey, Enum, Integer
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


class Preference(Base):
    __tablename__ = "preferences"

    id: Mapped[int] = mapped_column(primary_key=True)
    pilgrim_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    preferred_language: Mapped[PreferredLanguage] = mapped_column(
        Enum("English", "Hausa", "Yoruba", "Igbo", "Arabic", name="preferredlanguage", create_type=False),
        default=PreferredLanguage.English,
    )
    delivery_mode: Mapped[DeliveryMode] = mapped_column(
        Enum("Text", "Audio", "Text + Audio", name="deliverymode", create_type=False),
        default=DeliveryMode.Text,
    )
    font_size: Mapped[int] = mapped_column(Integer, default=16)
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
