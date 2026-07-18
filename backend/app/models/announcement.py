import enum

from sqlalchemy import String, Text, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class AnnouncementCategory(str, enum.Enum):
    emergency = "emergency"
    general = "general"
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
    category: Mapped[AnnouncementCategory] = mapped_column(Enum(AnnouncementCategory))
    language: Mapped[str] = mapped_column(String(10), default="en")
    priority: Mapped[AnnouncementPriority] = mapped_column(
        Enum(AnnouncementPriority), default=AnnouncementPriority.medium
    )
    publish_date: Mapped[str] = mapped_column(DateTime)
    expiry_date: Mapped[str] = mapped_column(DateTime)
    created_at: Mapped[str] = mapped_column(server_default=func.now())
    updated_at: Mapped[str] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
