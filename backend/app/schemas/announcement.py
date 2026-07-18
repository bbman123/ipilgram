from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.announcement import AnnouncementCategory, AnnouncementPriority


class AnnouncementCreate(BaseModel):
    title: str
    message: str
    category: AnnouncementCategory
    language: str = "en"
    priority: AnnouncementPriority = AnnouncementPriority.medium
    publish_date: datetime
    expiry_date: datetime


class AnnouncementUpdate(BaseModel):
    title: str | None = None
    message: str | None = None
    category: AnnouncementCategory | None = None
    language: str | None = None
    priority: AnnouncementPriority | None = None
    publish_date: datetime | None = None
    expiry_date: datetime | None = None


class AnnouncementResponse(BaseModel):
    id: int
    title: str
    message: str
    category: AnnouncementCategory
    language: str
    priority: AnnouncementPriority
    publish_date: datetime
    expiry_date: datetime
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class PaginatedAnnouncements(BaseModel):
    items: list[AnnouncementResponse]
    total: int
    page: int
    size: int
    pages: int
