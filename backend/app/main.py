import logging
import uuid

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from sqlalchemy.exc import IntegrityError

from app.core.config import get_settings
from app.core.rate_limit import limiter
from app.api.v1.router import api_router
from app.middleware import RequestIDMiddleware, SecurityHeadersMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.services.notification_engine import run_notification_engine

settings = get_settings()

logger = logging.getLogger("hajj_api")

_scheduler = None


@asynccontextmanager
async def lifespan(application: FastAPI):
    global _scheduler
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger

    _scheduler = BackgroundScheduler()
    _scheduler.add_job(
        run_notification_engine,
        trigger=IntervalTrigger(minutes=5),
        id="notification_engine",
        replace_existing=True,
    )
    _scheduler.start()
    logger.info("Notification engine scheduler started (every 5 minutes)")

    run_notification_engine()

    yield

    if _scheduler:
        _scheduler.shutdown(wait=False)
        logger.info("Notification engine scheduler stopped")

    from app.core.database import engine
    engine.dispose()
    logger.info("Database connections disposed")


TAGS_METADATA = [
    {"name": "Health", "description": "Service health checks"},
    {"name": "Dashboard", "description": "Dashboard statistics and analytics"},
    {"name": "Auth", "description": "User registration, login, token refresh, logout"},
    {"name": "Pilgrims", "description": "CRUD operations for pilgrim management (admin only)"},
    {"name": "Flights", "description": "Flight booking management with status tracking"},
    {"name": "Accommodations", "description": "Hotel and accommodation management"},
    {"name": "Transports", "description": "Ground transportation management"},
    {"name": "Packages", "description": "Hajj package management with component linking"},
    {"name": "Announcements", "description": "Announcement templates with placeholders and dynamic recipient resolution"},
    {"name": "Preferences", "description": "Pilgrim display and notification preferences"},
    {"name": "AI Personalization", "description": "AI-powered content simplification and translation (Gemini)"},
    {"name": "Text-to-Speech", "description": "Convert text to audio in multiple languages"},
    {"name": "Notifications", "description": "System-generated notifications for pilgrims based on package data"},
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
        lifespan=lifespan,
    )

    application.state.limiter = limiter
    application.add_exception_handler(RateLimitExceeded, _rate_limit_handler)

    application.add_middleware(RequestIDMiddleware)
    application.add_middleware(SecurityHeadersMiddleware)

    if settings.DEBUG:
        application.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
    else:
        application.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=["localhost", "127.0.0.1", ".onrender.com", ".railway.app", ".fly.dev"],
        )

    allowed_origins = settings.cors_origins_list
    if settings.DEBUG and "localhost" not in str(allowed_origins):
        allowed_origins = ["http://localhost:5173"]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
        expose_headers=["X-Request-ID", "X-Response-Time"],
    )

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            loc = " -> ".join(str(l) for l in error["loc"])
            errors.append({"field": loc, "message": error["msg"]})
        return JSONResponse(
            status_code=422,
            content={"success": False, "message": "Validation error", "data": None, "errors": errors},
        )

    @application.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        request_id = getattr(request.state, "request_id", "unknown")
        logger.error("IntegrityError [%s]: %s", request_id, str(exc.orig))
        return JSONResponse(
            status_code=409,
            content={"success": False, "message": "Database constraint violation", "data": None, "errors": None},
        )

    @application.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", "unknown")
        logger.error("Unhandled exception [%s]: %s", request_id, str(exc))
        if settings.DEBUG:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": str(exc), "data": None, "errors": None},
            )
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Internal server error", "data": None, "errors": None},
        )

    @application.get("/health", tags=["Health"])
    async def root_health():
        return {"status": "healthy"}

    application.include_router(api_router)

    return application


async def _rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"success": False, "message": "Rate limit exceeded. Please try again later.", "data": None, "errors": None},
    )


app = create_app()
