import enum
from datetime import datetime

from sqlalchemy import String, Text, Enum, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class TargetType(str, enum.Enum):
    all = "all"
    pilgrim = "pilgrim"
    package = "package"
    flight = "flight"
    accommodation = "accommodation"
    transport = "transport"


class AnnouncementPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class Announcement(Base):
    __tablename__ = "announcements"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    message: Mapped[str] = mapped_column(Text)
    priority: Mapped[AnnouncementPriority] = mapped_column(
        Enum(AnnouncementPriority), default=AnnouncementPriority.medium
    )
    target_type: Mapped[TargetType] = mapped_column(
        Enum(TargetType), default=TargetType.all
    )
    target_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    publish_date: Mapped[datetime] = mapped_column(DateTime)
    expiry_date: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
