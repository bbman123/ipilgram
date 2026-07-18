from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.user import Role


class PilgrimCreate(BaseModel):
    email: str = Field(..., min_length=5, max_length=255, description="Pilgrim email address", examples=["pilgrim@example.com"])
    password: str = Field(..., min_length=6, max_length=128, description="Login password", examples=["securepass123"])
    full_name: str = Field(..., min_length=1, max_length=255, description="Full name", examples=["Ahmed Mohammed"])
    phone: str | None = Field(default=None, max_length=50, description="Phone number", examples=["+2348012345678"])
    nationality: str | None = Field(default=None, max_length=100, description="Country of origin", examples=["Nigerian"])
    passport_number: str | None = Field(default=None, max_length=50, description="Passport number", examples=["A12345678"])
    emergency_contact: str | None = Field(default=None, max_length=500, description="Emergency contact details", examples=["+2348098765432"])


class PilgrimUpdate(BaseModel):
    email: str | None = Field(default=None, min_length=5, max_length=255, description="Email address")
    full_name: str | None = Field(default=None, min_length=1, max_length=255, description="Full name")
    phone: str | None = Field(default=None, max_length=50, description="Phone number")
    nationality: str | None = Field(default=None, max_length=100, description="Country of origin")
    passport_number: str | None = Field(default=None, max_length=50, description="Passport number")
    emergency_contact: str | None = Field(default=None, max_length=500, description="Emergency contact details")
    is_active: bool | None = Field(default=None, description="Account active status")
    package_id: int | None = Field(default=None, description="Assigned package ID")


class PilgrimResponse(BaseModel):
    id: int = Field(..., description="Unique pilgrim identifier")
    email: str = Field(..., description="Email address")
    full_name: str = Field(..., description="Full name")
    role: Role = Field(..., description="User role")
    is_active: bool = Field(..., description="Whether the account is active")
    phone: str | None = Field(default=None, description="Phone number")
    nationality: str | None = Field(default=None, description="Country of origin")
    passport_number: str | None = Field(default=None, description="Passport number")
    emergency_contact: str | None = Field(default=None, description="Emergency contact")
    package_id: int | None = Field(default=None, description="Assigned package ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class PaginatedPilgrims(BaseModel):
    items: list[PilgrimResponse] = Field(..., description="List of pilgrim records")
    total: int = Field(..., description="Total number of matching records")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
