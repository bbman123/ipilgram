from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.flight import FlightResponse
from app.schemas.accommodation import AccommodationResponse
from app.schemas.transport import TransportResponse


class PackageCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Package name", examples=["Premium Hajj 2026"])
    description: str | None = Field(default=None, max_length=2000, description="Package description")
    flight_id: int | None = Field(default=None, description="Associated flight ID")
    accommodation_id: int | None = Field(default=None, description="Associated accommodation ID")
    transport_id: int | None = Field(default=None, description="Associated transport ID")


class PackageUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255, description="Package name")
    description: str | None = Field(default=None, max_length=2000, description="Package description")
    flight_id: int | None = Field(default=None, description="Associated flight ID")
    accommodation_id: int | None = Field(default=None, description="Associated accommodation ID")
    transport_id: int | None = Field(default=None, description="Associated transport ID")


class PackageResponse(BaseModel):
    id: int = Field(..., description="Unique package identifier")
    name: str = Field(..., description="Package name")
    description: str | None = Field(default=None, description="Package description")
    flight_id: int | None = Field(default=None, description="Associated flight ID")
    accommodation_id: int | None = Field(default=None, description="Associated accommodation ID")
    transport_id: int | None = Field(default=None, description="Associated transport ID")
    pilgrim_count: int = Field(default=0, description="Number of pilgrims assigned to this package")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class PackageDetailResponse(BaseModel):
    id: int = Field(..., description="Unique package identifier")
    name: str = Field(..., description="Package name")
    description: str | None = Field(default=None, description="Package description")
    flight: FlightResponse | None = Field(default=None, description="Associated flight details")
    accommodation: AccommodationResponse | None = Field(default=None, description="Associated accommodation details")
    transport: TransportResponse | None = Field(default=None, description="Associated transport details")
    pilgrim_count: int = Field(default=0, description="Number of pilgrims assigned to this package")
    created_at: datetime = Field(..., description="Record creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class PaginatedPackages(BaseModel):
    items: list[PackageResponse] = Field(..., description="List of package records")
    total: int = Field(..., description="Total number of matching records")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
