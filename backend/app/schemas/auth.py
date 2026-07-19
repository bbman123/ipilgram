from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.user import Role


class UserRegister(BaseModel):
    email: str = Field(..., min_length=5, max_length=255, description="User email address", examples=["user@example.com"])
    password: str = Field(..., min_length=6, max_length=128, description="Plain text password", examples=["securepass123"])
    full_name: str = Field(..., min_length=1, max_length=255, description="Full name", examples=["Ibrahim Abdullahi"])


class UserLogin(BaseModel):
    email: str = Field(..., min_length=5, max_length=255, description="Registered email address")
    password: str = Field(..., min_length=6, max_length=128, description="Account password")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token for obtaining new access tokens")
    token_type: str = Field(default="bearer", description="Token type, always 'bearer'")


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., description="Valid refresh token")


class UserResponse(BaseModel):
    id: int = Field(..., description="Unique user identifier")
    email: str = Field(..., description="Email address")
    full_name: str = Field(..., description="Full name")
    role: Role = Field(..., description="User role (admin or pilgrim)")
    is_active: bool = Field(..., description="Whether the account is active")
    package_id: int | None = Field(None, description="Assigned package ID (pilgrims only)")
    phone: str | None = Field(None, description="Phone number")
    nationality: str | None = Field(None, description="Nationality")
    passport_number: str | None = Field(None, description="Passport number")
    emergency_contact: str | None = Field(None, description="Emergency contact details")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)
