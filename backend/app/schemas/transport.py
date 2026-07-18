from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.transport import TransportType


class TransportCreate(BaseModel):
    bus_number: str = Field(..., min_length=1, max_length=50, description="Vehicle number", examples=["KGH-123AB"])
    pickup_location: str = Field(..., min_length=1, max_length=255, description="Pickup location", examples=["Makkah Hotel Lobby"])
    destination: str = Field(..., min_length=1, max_length=255, description="Destination", examples=["Masjid al-Haram"])
    pickup_time: datetime = Field(..., description="Scheduled pickup time (UTC)")
    driver_name: str = Field(..., min_length=1, max_length=255, description="Driver full name", examples=["Ali Hassan"])
    driver_phone: str = Field(..., min_length=5, max_length=50, description="Driver phone number", examples=["+2348012345678"])
    transport_type: TransportType = Field(default=TransportType.bus, description="Vehicle type")


class TransportUpdate(BaseModel):
    bus_number: str | None = Field(default=None, min_length=1, max_length=50, description="Vehicle number")
    pickup_location: str | None = Field(default=None, min_length=1, max_length=255, description="Pickup location")
    destination: str | None = Field(default=None, min_length=1, max_length=255, description="Destination")
    pickup_time: datetime | None = Field(default=None, description="Pickup time")
    driver_name: str | None = Field(default=None, min_length=1, max_length=255, description="Driver name")
    driver_phone: str | None = Field(default=None, min_length=5, max_length=50, description="Driver phone")
    transport_type: TransportType | None = Field(default=None, description="Vehicle type")


class TransportResponse(BaseModel):
    id: int = Field(..., description="Unique transport identifier")
    bus_number: str = Field(..., description="Vehicle number")
    pickup_location: str = Field(..., description="Pickup location")
    destination: str = Field(..., description="Destination")
    pickup_time: datetime = Field(..., description="Scheduled pickup time (UTC)")
    driver_name: str = Field(..., description="Driver full name")
    driver_phone: str = Field(..., description="Driver phone number")
    transport_type: TransportType = Field(..., description="Vehicle type")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class PaginatedTransports(BaseModel):
    items: list[TransportResponse] = Field(..., description="List of transport records")
    total: int = Field(..., description="Total number of matching records")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
