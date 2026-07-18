from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.announcement import TargetType, AnnouncementPriority


class AnnouncementCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Announcement title", examples=["Flight Delay Notice"])
    message: str = Field(..., min_length=1, max_length=5000, description="Announcement content", examples=["Flight NA-101 has been delayed by 2 hours."])
    priority: AnnouncementPriority = Field(default=AnnouncementPriority.medium, description="Priority level")
    target_type: TargetType = Field(default=TargetType.all, description="Target audience")
    target_id: int | None = Field(default=None, description="Target entity ID (required when target_type is not 'all')")
    publish_date: datetime = Field(..., description="When the announcement becomes visible (UTC)")
    expiry_date: datetime = Field(..., description="When the announcement expires (UTC)")

    @model_validator(mode="after")
    def validate_target_id(self):
        if self.target_type != TargetType.all and self.target_id is None:
            raise ValueError(f"target_id is required when target_type is '{self.target_type.value}'")
        if self.target_type == TargetType.all and self.target_id is not None:
            raise ValueError("target_id must not be set when target_type is 'all'")
        return self


class AnnouncementUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255, description="Announcement title")
    message: str | None = Field(default=None, min_length=1, max_length=5000, description="Announcement content")
    priority: AnnouncementPriority | None = Field(default=None, description="Priority level")
    target_type: TargetType | None = Field(default=None, description="Target audience")
    target_id: int | None = Field(default=None, description="Target entity ID")
    publish_date: datetime | None = Field(default=None, description="Publish datetime")
    expiry_date: datetime | None = Field(default=None, description="Expiry datetime")

    @model_validator(mode="after")
    def validate_target(self):
        if self.target_type is not None and self.target_type != TargetType.all and self.target_id is None:
            raise ValueError(f"target_id is required when target_type is '{self.target_type.value}'")
        if self.target_type == TargetType.all:
            self.target_id = None
        return self


class AnnouncementResponse(BaseModel):
    id: int = Field(..., description="Unique announcement identifier")
    title: str = Field(..., description="Announcement title")
    message: str = Field(..., description="Announcement content")
    priority: AnnouncementPriority = Field(..., description="Priority level")
    target_type: TargetType = Field(..., description="Target audience")
    target_id: int | None = Field(default=None, description="Target entity ID")
    publish_date: datetime = Field(..., description="Publish datetime (UTC)")
    expiry_date: datetime = Field(..., description="Expiry datetime (UTC)")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class PaginatedAnnouncements(BaseModel):
    items: list[AnnouncementResponse] = Field(..., description="List of announcement records")
    total: int = Field(..., description="Total number of matching records")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
