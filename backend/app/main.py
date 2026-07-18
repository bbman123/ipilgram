from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from app.core.config import get_settings
from app.api.v1.router import api_router

settings = get_settings()

TAGS_METADATA = [
    {"name": "Health", "description": "Service health checks"},
    {"name": "Auth", "description": "User registration, login, token refresh, logout"},
    {"name": "Pilgrims", "description": "CRUD operations for pilgrim management (admin only)"},
    {"name": "Flights", "description": "Flight booking management with status tracking"},
    {"name": "Accommodations", "description": "Hotel and accommodation management"},
    {"name": "Transports", "description": "Ground transportation management"},
    {"name": "Announcements", "description": "Multi-language Hajj announcements with priority levels"},
    {"name": "Preferences", "description": "Pilgrim display and notification preferences"},
    {"name": "AI Personalization", "description": "AI-powered content simplification and translation (Gemini)"},
    {"name": "Text-to-Speech", "description": "Convert text to audio in multiple languages"},
    {"name": "Notifications", "description": "Push notification delivery and device token management"},
]


def create_app() -> FastAPI:
    application = FastAPI(
        title="Hajj Pilgrims Management API",
        description=(
            "Privacy-preserving AI-based multimodal mobile information delivery system "
            "for Hajj pilgrims. Provides flight, accommodation, transport, and announcement "
            "management with AI-powered personalization and multi-language support."
        ),
        version=settings.APP_VERSION,
        openapi_tags=TAGS_METADATA,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            loc = " -> ".join(str(l) for l in error["loc"])
            errors.append({"field": loc, "message": error["msg"]})
        return JSONResponse(
            status_code=422,
            content={"detail": "Validation error", "errors": errors},
        )

    @application.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=409,
            content={"detail": "Database constraint violation. The request conflicts with existing data."},
        )

    @application.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        if settings.DEBUG:
            return JSONResponse(
                status_code=500,
                content={"detail": f"Internal server error: {str(exc)}"},
            )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

    application.include_router(api_router)

    return application


app = create_app()
