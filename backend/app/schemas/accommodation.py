from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AccommodationCreate(BaseModel):
    pilgrim_id: int
    hotel_name: str
    city: str
    building: str | None = None
    floor: str | None = None
    room_number: str
    bed_number: str | None = None
    address: str | None = None
    check_in: datetime
    check_out: datetime


class AccommodationUpdate(BaseModel):
    pilgrim_id: int | None = None
    hotel_name: str | None = None
    city: str | None = None
    building: str | None = None
    floor: str | None = None
    room_number: str | None = None
    bed_number: str | None = None
    address: str | None = None
    check_in: datetime | None = None
    check_out: datetime | None = None


class AccommodationResponse(BaseModel):
    id: int
    pilgrim_id: int
    hotel_name: str
    city: str
    building: str | None
    floor: str | None
    room_number: str
    bed_number: str | None
    address: str | None
    check_in: datetime
    check_out: datetime
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class AccommodationWithPilgrim(AccommodationResponse):
    pilgrim_name: str | None = None
    pilgrim_email: str | None = None


class PaginatedAccommodations(BaseModel):
    items: list[AccommodationWithPilgrim]
    total: int
    page: int
    size: int
    pages: int
