from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.preference import PreferredLanguage, DeliveryMode


class PreferenceCreate(BaseModel):
    pilgrim_id: int
    preferred_language: PreferredLanguage = PreferredLanguage.english
    delivery_mode: DeliveryMode = DeliveryMode.text
    font_size: int = Field(default=16, ge=8, le=48, description="Font size (8-48)")
    notifications_enabled: bool = True


class PreferenceUpdate(BaseModel):
    preferred_language: PreferredLanguage | None = None
    delivery_mode: DeliveryMode | None = None
    font_size: int | None = Field(default=None, ge=8, le=48, description="Font size (8-48)")
    notifications_enabled: bool | None = None


class PreferenceResponse(BaseModel):
    id: int
    pilgrim_id: int
    preferred_language: PreferredLanguage
    delivery_mode: DeliveryMode
    font_size: int
    notifications_enabled: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PreferenceWithPilgrim(PreferenceResponse):
    pilgrim_name: str | None = None
    pilgrim_email: str | None = None


class PaginatedPreferences(BaseModel):
    items: list[PreferenceWithPilgrim] = Field(..., description="List of preference records")
    total: int = Field(..., description="Total number of matching records")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
