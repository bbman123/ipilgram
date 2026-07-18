from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user import Role


class PilgrimCreate(BaseModel):
    email: str
    password: str
    full_name: str
    phone: str | None = None
    nationality: str | None = None
    passport_number: str | None = None
    emergency_contact: str | None = None


class PilgrimUpdate(BaseModel):
    email: str | None = None
    full_name: str | None = None
    phone: str | None = None
    nationality: str | None = None
    passport_number: str | None = None
    emergency_contact: str | None = None
    is_active: bool | None = None


class PilgrimResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: Role
    is_active: bool
    phone: str | None
    nationality: str | None
    passport_number: str | None
    emergency_contact: str | None
    created_at: str
    updated_at: str

    model_config = ConfigDict(from_attributes=True)


class PaginatedPilgrims(BaseModel):
    items: list[PilgrimResponse]
    total: int
    page: int
    size: int
    pages: int
