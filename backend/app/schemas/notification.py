from pydantic import BaseModel, Field

from app.models.notification import NotificationType, NotificationStatus


class SendNotificationRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Notification title", examples=["Flight Update"])
    body: str = Field(..., min_length=1, max_length=2000, description="Notification message body", examples=["Your flight has been rescheduled."])
    notification_type: NotificationType = Field(..., description="Notification category")
    pilgrim_ids: list[int] | None = Field(default=None, description="Target pilgrim IDs. Null or empty = broadcast to all active pilgrims.")


class NotificationResponse(BaseModel):
    id: int = Field(..., description="Unique notification identifier")
    title: str = Field(..., description="Notification title")
    body: str = Field(..., description="Notification message body")
    notification_type: NotificationType = Field(..., description="Notification category")
    pilgrim_id: int | None = Field(default=None, description="Target pilgrim ID (null for broadcasts)")
    is_broadcast: bool = Field(..., description="Whether this was a broadcast notification")
    status: NotificationStatus = Field(..., description="Delivery status")
    sent_at: str | None = Field(default=None, description="Timestamp when sent")
    created_at: str = Field(..., description="Record creation timestamp")

    model_config = {"from_attributes": True}


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

    model_config = {"from_attributes": True}
