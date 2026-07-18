from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str


class ValidationErrorDetail(BaseModel):
    field: str
    message: str


class ValidationErrorResponse(BaseModel):
    detail: str = "Validation error"
    errors: list[ValidationErrorDetail]
