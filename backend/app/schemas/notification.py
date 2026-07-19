from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.notification import NotificationType, NotificationStatus


class NotificationResponse(BaseModel):
    id: int = Field(..., description="Unique notification identifier")
    pilgrim_id: int = Field(..., description="Target pilgrim ID")
    title: str = Field(..., description="Notification title")
    message: str = Field(..., description="Notification message body")
    notification_type: NotificationType = Field(..., description="Notification category")
    status: NotificationStatus = Field(..., description="Delivery status")
    scheduled_time: datetime | None = Field(default=None, description="When the notification is scheduled for")
    sent_at: datetime | None = Field(default=None, description="Timestamp when sent")
    read_at: datetime | None = Field(default=None, description="Timestamp when read by pilgrim")
    delivery_mode: str | None = Field(default=None, description="Delivery format (text, audio, text_and_audio)")
    language: str | None = Field(default=None, description="Notification language")
    audio_url: str | None = Field(default=None, description="URL to audio file if generated")
    source_type: str | None = Field(default=None, description="Source entity type (flight, accommodation, transport, package)")
    source_id: int | None = Field(default=None, description="Source entity ID")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class PaginatedNotifications(BaseModel):
    items: list[NotificationResponse] = Field(..., description="List of notification records")
    total: int = Field(..., description="Total number of matching records")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")


class DeviceTokenRequest(BaseModel):
    token: str = Field(..., min_length=1, max_length=512, description="FCM/APNs device token", examples=["device_token_abc123"])
    platform: str = Field(default="android", max_length=20, description="Device platform", examples=["android"])


class DeviceTokenResponse(BaseModel):
    id: int = Field(..., description="Unique device token identifier")
    pilgrim_id: int = Field(..., description="Owner pilgrim ID")
    token: str = Field(..., description="Device token value")
    platform: str = Field(..., description="Device platform")
    is_active: bool = Field(..., description="Whether the token is active")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)
