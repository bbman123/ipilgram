from fastapi import APIRouter
from pydantic import BaseModel

from app.schemas.response import success_response

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str


@router.get(
    "/health",
    summary="Service health check",
    description="Returns the health status of the API service. No authentication required.",
    responses={
        200: {"description": "Service is healthy", "model": HealthResponse},
    },
)
def health_check():
    """Check if the API service is running and healthy."""
    return success_response(data=HealthResponse(status="healthy").model_dump(), message="Service is healthy")
