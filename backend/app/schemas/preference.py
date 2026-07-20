from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.preference import PreferredLanguage, DeliveryMode


class PreferenceCreate(BaseModel):
    pilgrim_id: int = Field(..., description="Pilgrim user ID to set preferences for", examples=[1])
    preferred_language: PreferredLanguage = Field(
        default=PreferredLanguage.English,
        description="Preferred display and notification language",
        examples=["English"],
    )
    delivery_mode: DeliveryMode = Field(
        default=DeliveryMode.Text,
        description="Preferred content delivery format",
        examples=["Text + Audio"],
    )
    font_size: int = Field(default=16, ge=8, le=48, description="Display font size (8-48)", examples=[16])
    notifications_enabled: bool = Field(default=True, description="Whether push notifications are enabled", examples=[True])


class PreferenceUpdate(BaseModel):
    preferred_language: PreferredLanguage | None = Field(default=None, description="Preferred display and notification language")
    delivery_mode: DeliveryMode | None = Field(default=None, description="Preferred content delivery format")
    font_size: int | None = Field(default=None, ge=8, le=48, description="Display font size (8-48)")
    notifications_enabled: bool | None = Field(default=None, description="Whether push notifications are enabled")


class PreferenceResponse(BaseModel):
    id: int = Field(..., description="Unique preference identifier")
    pilgrim_id: int = Field(..., description="Pilgrim user ID")
    preferred_language: PreferredLanguage = Field(..., description="Preferred display and notification language")
    delivery_mode: DeliveryMode = Field(..., description="Preferred content delivery format")
    font_size: int = Field(..., description="Display font size (8-48)")
    notifications_enabled: bool = Field(..., description="Whether push notifications are enabled")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class PreferenceWithPilgrim(PreferenceResponse):
    pilgrim_name: str | None = Field(default=None, description="Pilgrim full name")
    pilgrim_email: str | None = Field(default=None, description="Pilgrim email address")


class PaginatedPreferences(BaseModel):
    items: list[PreferenceWithPilgrim] = Field(..., description="List of preference records")
    total: int = Field(..., description="Total number of matching records")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
