from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.announcement import TargetType, AnnouncementPriority


AVAILABLE_PLACEHOLDERS = [
    "{{pilgrim_name}}",
    "{{package_name}}",
    "{{flight_number}}",
    "{{airline}}",
    "{{departure_airport}}",
    "{{arrival_airport}}",
    "{{departure_time}}",
    "{{arrival_time}}",
    "{{gate}}",
    "{{seat}}",
    "{{hotel_name}}",
    "{{city}}",
    "{{room_number}}",
    "{{check_in_time}}",
    "{{check_out_time}}",
    "{{pickup_location}}",
    "{{destination}}",
    "{{pickup_time}}",
    "{{driver_name}}",
    "{{driver_phone}}",
]


class AnnouncementCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Announcement template title")
    message_template: str = Field(
        ..., min_length=1, max_length=5000,
        description="Message template with optional placeholders: {{pilgrim_name}}, {{flight_number}}, {{departure_airport}}, {{departure_time}}, {{hotel_name}}, {{room_number}}, {{check_in_time}}, {{check_out_time}}, {{pickup_location}}, {{pickup_time}}, {{driver_name}}",
        examples=["Hello {{pilgrim_name}}, your flight {{flight_number}} departs from {{departure_airport}} at {{departure_time}}."],
    )
    priority: AnnouncementPriority = Field(default=AnnouncementPriority.medium, description="Priority level")
    target_type: TargetType = Field(default=TargetType.all, description="Target audience")
    target_id: int | None = Field(default=None, description="Target entity ID (required when target_type is not 'all')")
    publish_date: datetime = Field(..., description="When the announcement becomes visible (UTC)")
    expiry_date: datetime = Field(..., description="When the announcement expires (UTC)")
    include_package_details: bool = Field(default=False, description="Include package info in personalized message")
    include_flight_details: bool = Field(default=False, description="Include flight info in personalized message")
    include_transport_details: bool = Field(default=False, description="Include transport info in personalized message")
    include_accommodation_details: bool = Field(default=False, description="Include accommodation info in personalized message")
    send_as_notification: bool = Field(default=False, description="Also send as push notification to targeted pilgrims")

    @model_validator(mode="after")
    def validate_target_id(self):
        if self.target_type != TargetType.all and self.target_id is None:
            raise ValueError(f"target_id is required when target_type is '{self.target_type.value}'")
        if self.target_type == TargetType.all and self.target_id is not None:
            raise ValueError("target_id must not be set when target_type is 'all'")
        return self


class AnnouncementUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255, description="Announcement template title")
    message_template: str | None = Field(default=None, min_length=1, max_length=5000, description="Message template with placeholders")
    priority: AnnouncementPriority | None = Field(default=None, description="Priority level")
    target_type: TargetType | None = Field(default=None, description="Target audience")
    target_id: int | None = Field(default=None, description="Target entity ID")
    publish_date: datetime | None = Field(default=None, description="Publish datetime")
    expiry_date: datetime | None = Field(default=None, description="Expiry datetime")
    include_package_details: bool | None = Field(default=None, description="Include package info")
    include_flight_details: bool | None = Field(default=None, description="Include flight info")
    include_transport_details: bool | None = Field(default=None, description="Include transport info")
    include_accommodation_details: bool | None = Field(default=None, description="Include accommodation info")
    send_as_notification: bool | None = Field(default=None, description="Also send as push notification")

    @model_validator(mode="after")
    def validate_target(self):
        if self.target_type is not None and self.target_type != TargetType.all and self.target_id is None:
            raise ValueError(f"target_id is required when target_type is '{self.target_type.value}'")
        if self.target_type == TargetType.all:
            self.target_id = None
        return self


class AnnouncementResponse(BaseModel):
    id: int = Field(..., description="Unique announcement identifier")
    title: str = Field(..., description="Announcement template title")
    message_template: str = Field(..., description="Message template with placeholders")
    priority: AnnouncementPriority = Field(..., description="Priority level")
    target_type: TargetType = Field(..., description="Target audience")
    target_id: int | None = Field(default=None, description="Target entity ID")
    publish_date: datetime = Field(..., description="Publish datetime (UTC)")
    expiry_date: datetime = Field(..., description="Expiry datetime (UTC)")
    include_package_details: bool = Field(..., description="Include package info in personalized message")
    include_flight_details: bool = Field(..., description="Include flight info in personalized message")
    include_transport_details: bool = Field(..., description="Include transport info in personalized message")
    include_accommodation_details: bool = Field(..., description="Include accommodation info in personalized message")
    send_as_notification: bool = Field(..., description="Also send as push notification")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class PersonalizedAnnouncement(BaseModel):
    id: int = Field(..., description="Announcement ID")
    title: str = Field(..., description="Announcement title")
    message: str = Field(..., description="Personalized message with placeholders replaced")
    priority: AnnouncementPriority = Field(..., description="Priority level")
    publish_date: datetime = Field(..., description="Publish datetime (UTC)")
    expiry_date: datetime = Field(..., description="Expiry datetime (UTC)")
    simplified: bool = Field(default=False, description="Whether the message was simplified by AI")
    translated: bool = Field(default=False, description="Whether the message was translated by AI")
    language: str = Field(default="English", description="Language of the personalized message")
    audio_url: str | None = Field(default=None, description="URL to audio file if generated")

    model_config = ConfigDict(from_attributes=True)


class PaginatedAnnouncements(BaseModel):
    items: list[AnnouncementResponse] = Field(..., description="List of announcement records")
    total: int = Field(..., description="Total number of matching records")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
