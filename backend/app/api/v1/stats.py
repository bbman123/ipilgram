from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func

from app.core.database import get_db
from app.api.deps import require_role
from app.models.user import User, Role
from app.models.flight import Flight
from app.models.accommodation import Accommodation
from app.models.transport import Transport
from app.models.package import Package
from app.models.announcement import Announcement
from app.models.notification import Notification
from app.models.preference import Preference
from app.schemas.response import success_response

router = APIRouter(tags=["Dashboard"])


class DashboardStats(BaseModel):
    total_pilgrims: int
    total_packages: int
    total_flights: int
    total_accommodations: int
    total_transports: int
    total_announcements: int
    total_notifications: int
    total_preferences: int
    active_pilgrims: int


@router.get(
    "/stats",
    summary="Get dashboard statistics",
    description="Returns aggregate counts for all entities. Admin only.",
    responses={
        200: {"description": "Dashboard statistics"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def get_dashboard_stats(
    db=Depends(get_db),
    _admin=Depends(require_role(Role.admin)),
):
    total_pilgrims = db.query(func.count(User.id)).filter(User.role == Role.pilgrim).scalar() or 0
    active_pilgrims = db.query(func.count(User.id)).filter(User.role == Role.pilgrim, User.is_active == True).scalar() or 0
    total_packages = db.query(func.count(Package.id)).scalar() or 0
    total_flights = db.query(func.count(Flight.id)).scalar() or 0
    total_accommodations = db.query(func.count(Accommodation.id)).scalar() or 0
    total_transports = db.query(func.count(Transport.id)).scalar() or 0
    total_announcements = db.query(func.count(Announcement.id)).scalar() or 0
    total_notifications = db.query(func.count(Notification.id)).scalar() or 0
    total_preferences = db.query(func.count(Preference.id)).scalar() or 0

    return success_response(
        data=DashboardStats(
            total_pilgrims=total_pilgrims,
            total_packages=total_packages,
            total_flights=total_flights,
            total_accommodations=total_accommodations,
            total_transports=total_transports,
            total_announcements=total_announcements,
            total_notifications=total_notifications,
            total_preferences=total_preferences,
            active_pilgrims=active_pilgrims,
        ).model_dump(),
        message="Dashboard statistics retrieved successfully",
    )
