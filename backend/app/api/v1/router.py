from fastapi import APIRouter

from app.api.v1 import health, auth, pilgrims, flights, accommodations, transports, announcements, preferences, personalize, tts

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router)
api_router.include_router(pilgrims.router)
api_router.include_router(flights.router)
api_router.include_router(accommodations.router)
api_router.include_router(transports.router)
api_router.include_router(announcements.router)
api_router.include_router(preferences.router)
api_router.include_router(personalize.router)
api_router.include_router(tts.router)
