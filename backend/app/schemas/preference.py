from pydantic import BaseModel, ConfigDict

from app.models.preference import PreferredLanguage, DeliveryMode


class PreferenceCreate(BaseModel):
    pilgrim_id: int
    preferred_language: PreferredLanguage = PreferredLanguage.english
    delivery_mode: DeliveryMode = DeliveryMode.text
    font_size: int = 16
    notifications_enabled: bool = True


class PreferenceUpdate(BaseModel):
    preferred_language: PreferredLanguage | None = None
    delivery_mode: DeliveryMode | None = None
    font_size: int | None = None
    notifications_enabled: bool | None = None


class PreferenceResponse(BaseModel):
    id: int
    pilgrim_id: int
    preferred_language: PreferredLanguage
    delivery_mode: DeliveryMode
    font_size: int
    notifications_enabled: bool
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class PreferenceWithPilgrim(PreferenceResponse):
    pilgrim_name: str | None = None
    pilgrim_email: str | None = None


class PaginatedPreferences(BaseModel):
    items: list[PreferenceWithPilgrim]
    total: int
    page: int
    size: int
    pages: int
