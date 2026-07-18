from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.flight import FlightStatus


class FlightCreate(BaseModel):
    airline: str = Field(..., min_length=1, max_length=255, description="Airline name", examples=["Nigerian Airlines"])
    flight_number: str = Field(..., min_length=1, max_length=50, description="Flight number", examples=["NA-101"])
    departure_airport: str = Field(..., min_length=1, max_length=100, description="Departure airport code", examples=["ABV"])
    arrival_airport: str = Field(..., min_length=1, max_length=100, description="Arrival airport code", examples=["JED"])
    departure_datetime: datetime = Field(..., description="Departure date and time (UTC)")
    arrival_datetime: datetime = Field(..., description="Arrival date and time (UTC)")
    gate: str | None = Field(default=None, max_length=20, description="Boarding gate", examples=["B12"])
    seat_number: str | None = Field(default=None, max_length=20, description="Seat assignment", examples=["14A"])
    status: FlightStatus = Field(default=FlightStatus.scheduled, description="Flight status")


class FlightUpdate(BaseModel):
    airline: str | None = Field(default=None, min_length=1, max_length=255, description="Airline name")
    flight_number: str | None = Field(default=None, min_length=1, max_length=50, description="Flight number")
    departure_airport: str | None = Field(default=None, min_length=1, max_length=100, description="Departure airport")
    arrival_airport: str | None = Field(default=None, min_length=1, max_length=100, description="Arrival airport")
    departure_datetime: datetime | None = Field(default=None, description="Departure datetime")
    arrival_datetime: datetime | None = Field(default=None, description="Arrival datetime")
    gate: str | None = Field(default=None, max_length=20, description="Boarding gate")
    seat_number: str | None = Field(default=None, max_length=20, description="Seat assignment")
    status: FlightStatus | None = Field(default=None, description="Flight status")


class FlightResponse(BaseModel):
    id: int = Field(..., description="Unique flight identifier")
    airline: str = Field(..., description="Airline name")
    flight_number: str = Field(..., description="Flight number")
    departure_airport: str = Field(..., description="Departure airport")
    arrival_airport: str = Field(..., description="Arrival airport")
    departure_datetime: datetime = Field(..., description="Departure datetime (UTC)")
    arrival_datetime: datetime = Field(..., description="Arrival datetime (UTC)")
    gate: str | None = Field(default=None, description="Boarding gate")
    seat_number: str | None = Field(default=None, description="Seat assignment")
    status: FlightStatus = Field(..., description="Current flight status")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class PaginatedFlights(BaseModel):
    items: list[FlightResponse] = Field(..., description="List of flight records")
    total: int = Field(..., description="Total number of matching records")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
