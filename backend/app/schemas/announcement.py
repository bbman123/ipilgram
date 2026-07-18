from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.announcement import AnnouncementCategory, AnnouncementPriority


class AnnouncementCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Announcement title", examples=["Flight Delay Notice"])
    message: str = Field(..., min_length=1, max_length=5000, description="Announcement content", examples=["Flight NA-101 has been delayed by 2 hours."])
    category: AnnouncementCategory = Field(..., description="Announcement category")
    language: str = Field(default="en", max_length=10, description="Language code (en, ha, ar, yo, ig)", examples=["en"])
    priority: AnnouncementPriority = Field(default=AnnouncementPriority.medium, description="Priority level")
    publish_date: datetime = Field(..., description="When the announcement becomes visible (UTC)")
    expiry_date: datetime = Field(..., description="When the announcement expires (UTC)")


class AnnouncementUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255, description="Announcement title")
    message: str | None = Field(default=None, min_length=1, max_length=5000, description="Announcement content")
    category: AnnouncementCategory | None = Field(default=None, description="Announcement category")
    language: str | None = Field(default=None, max_length=10, description="Language code")
    priority: AnnouncementPriority | None = Field(default=None, description="Priority level")
    publish_date: datetime | None = Field(default=None, description="Publish datetime")
    expiry_date: datetime | None = Field(default=None, description="Expiry datetime")


class AnnouncementResponse(BaseModel):
    id: int = Field(..., description="Unique announcement identifier")
    title: str = Field(..., description="Announcement title")
    message: str = Field(..., description="Announcement content")
    category: AnnouncementCategory = Field(..., description="Category")
    language: str = Field(..., description="Language code")
    priority: AnnouncementPriority = Field(..., description="Priority level")
    publish_date: datetime = Field(..., description="Publish datetime (UTC)")
    expiry_date: datetime = Field(..., description="Expiry datetime (UTC)")
    created_at: str = Field(..., description="Record creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class PaginatedAnnouncements(BaseModel):
    items: list[AnnouncementResponse] = Field(..., description="List of announcement records")
    total: int = Field(..., description="Total number of matching records")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
