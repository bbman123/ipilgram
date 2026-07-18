from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AccommodationCreate(BaseModel):
    pilgrim_id: int = Field(..., description="Pilgrim user ID")
    hotel_name: str = Field(..., min_length=1, max_length=255, description="Hotel name", examples=["Hilton Suites Makkah"])
    city: str = Field(..., min_length=1, max_length=100, description="City name", examples=["Makkah"])
    building: str | None = Field(default=None, max_length=100, description="Building name or number", examples=["Tower A"])
    floor: str | None = Field(default=None, max_length=20, description="Floor number", examples=["5"])
    room_number: str = Field(..., min_length=1, max_length=20, description="Room number", examples=["501"])
    bed_number: str | None = Field(default=None, max_length=20, description="Bed number", examples=["B2"])
    address: str | None = Field(default=None, max_length=500, description="Full address", examples=["Al Aziziyah District, Makkah"])
    check_in: datetime = Field(..., description="Check-in date and time (UTC)")
    check_out: datetime = Field(..., description="Check-out date and time (UTC)")


class AccommodationUpdate(BaseModel):
    pilgrim_id: int | None = Field(default=None, description="Reassign to another pilgrim")
    hotel_name: str | None = Field(default=None, min_length=1, max_length=255, description="Hotel name")
    city: str | None = Field(default=None, min_length=1, max_length=100, description="City name")
    building: str | None = Field(default=None, max_length=100, description="Building name")
    floor: str | None = Field(default=None, max_length=20, description="Floor number")
    room_number: str | None = Field(default=None, min_length=1, max_length=20, description="Room number")
    bed_number: str | None = Field(default=None, max_length=20, description="Bed number")
    address: str | None = Field(default=None, max_length=500, description="Full address")
    check_in: datetime | None = Field(default=None, description="Check-in datetime")
    check_out: datetime | None = Field(default=None, description="Check-out datetime")


class AccommodationResponse(BaseModel):
    id: int = Field(..., description="Unique accommodation identifier")
    pilgrim_id: int = Field(..., description="Assigned pilgrim ID")
    hotel_name: str = Field(..., description="Hotel name")
    city: str = Field(..., description="City name")
    building: str | None = Field(default=None, description="Building name")
    floor: str | None = Field(default=None, description="Floor number")
    room_number: str = Field(..., description="Room number")
    bed_number: str | None = Field(default=None, description="Bed number")
    address: str | None = Field(default=None, description="Full address")
    check_in: datetime = Field(..., description="Check-in datetime (UTC)")
    check_out: datetime = Field(..., description="Check-out datetime (UTC)")
    created_at: str = Field(..., description="Record creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class AccommodationWithPilgrim(AccommodationResponse):
    pilgrim_name: str | None = Field(default=None, description="Pilgrim full name")
    pilgrim_email: str | None = Field(default=None, description="Pilgrim email address")


class PaginatedAccommodations(BaseModel):
    items: list[AccommodationWithPilgrim] = Field(..., description="List of accommodation records")
    total: int = Field(..., description="Total number of matching records")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
