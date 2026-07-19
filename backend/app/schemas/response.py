from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response envelope."""
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Human-readable status message")
    data: T | None = Field(default=None, description="Response payload")
    errors: Any | None = Field(default=None, description="Error details if success=false")


class PaginatedData(BaseModel, Generic[T]):
    """Paginated list data wrapper."""
    items: list[T] = Field(..., description="List of records")
    total: int = Field(..., description="Total number of matching records")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")


def success_response(data: Any = None, message: str = "Success") -> dict:
    return {"success": True, "message": message, "data": data, "errors": None}


def error_response(message: str = "Error", errors: Any = None, status_code: int = 400) -> dict:
    return {"success": False, "message": message, "data": None, "errors": errors}
