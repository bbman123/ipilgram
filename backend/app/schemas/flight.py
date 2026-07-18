from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.flight import FlightStatus


class FlightCreate(BaseModel):
    pilgrim_id: int
    airline: str
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_datetime: datetime
    arrival_datetime: datetime
    gate: str | None = None
    seat_number: str | None = None
    status: FlightStatus = FlightStatus.scheduled


class FlightUpdate(BaseModel):
    pilgrim_id: int | None = None
    airline: str | None = None
    flight_number: str | None = None
    departure_airport: str | None = None
    arrival_airport: str | None = None
    departure_datetime: datetime | None = None
    arrival_datetime: datetime | None = None
    gate: str | None = None
    seat_number: str | None = None
    status: FlightStatus | None = None


class FlightResponse(BaseModel):
    id: int
    pilgrim_id: int
    airline: str
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_datetime: datetime
    arrival_datetime: datetime
    gate: str | None
    seat_number: str | None
    status: FlightStatus
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class FlightWithPilgrim(FlightResponse):
    pilgrim_name: str | None = None
    pilgrim_email: str | None = None


class PaginatedFlights(BaseModel):
    items: list[FlightWithPilgrim]
    total: int
    page: int
    size: int
    pages: int
