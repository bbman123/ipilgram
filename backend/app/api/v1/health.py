from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    status: str


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Service health check",
    description="Returns the health status of the API service. No authentication required.",
    responses={
        200: {"description": "Service is healthy", "model": HealthResponse},
    },
)
def health_check():
    """Check if the API service is running and healthy."""
    return {"status": "healthy"}
