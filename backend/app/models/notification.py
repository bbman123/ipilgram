import enum
from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime, Enum, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class NotificationType(str, enum.Enum):
    flight_reminder = "flight_reminder"
    accommodation_checkin = "accommodation_checkin"
    accommodation_checkout = "accommodation_checkout"
    transport_reminder = "transport_reminder"
    return_flight = "return_flight"
    emergency = "emergency"
    broadcast = "broadcast"
    announcement = "announcement"


class NotificationStatus(str, enum.Enum):
    pending = "pending"
    scheduled = "scheduled"
    sent = "sent"
    failed = "failed"
    read = "read"


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    pilgrim_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(Text)
    notification_type: Mapped[NotificationType] = mapped_column(Enum(NotificationType))
    status: Mapped[NotificationStatus] = mapped_column(
        Enum(NotificationStatus), default=NotificationStatus.pending
    )
    scheduled_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    read_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    delivery_mode: Mapped[str | None] = mapped_column(String(20), nullable=True, default="text")
    language: Mapped[str | None] = mapped_column(String(20), nullable=True, default="English")
    audio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    source_type: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    source_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class DeviceToken(Base):
    __tablename__ = "device_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    pilgrim_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    token: Mapped[str] = mapped_column(String(512), unique=True)
    platform: Mapped[str] = mapped_column(String(20), default="android")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
