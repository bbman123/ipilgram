from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.transport import TransportType


class TransportCreate(BaseModel):
    pilgrim_id: int
    bus_number: str
    pickup_location: str
    destination: str
    pickup_time: datetime
    driver_name: str
    driver_phone: str
    transport_type: TransportType = TransportType.bus


class TransportUpdate(BaseModel):
    pilgrim_id: int | None = None
    bus_number: str | None = None
    pickup_location: str | None = None
    destination: str | None = None
    pickup_time: datetime | None = None
    driver_name: str | None = None
    driver_phone: str | None = None
    transport_type: TransportType | None = None


class TransportResponse(BaseModel):
    id: int
    pilgrim_id: int
    bus_number: str
    pickup_location: str
    destination: str
    pickup_time: datetime
    driver_name: str
    driver_phone: str
    transport_type: TransportType
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class TransportWithPilgrim(TransportResponse):
    pilgrim_name: str | None = None
    pilgrim_email: str | None = None


class PaginatedTransports(BaseModel):
    items: list[TransportWithPilgrim]
    total: int
    page: int
    size: int
    pages: int
