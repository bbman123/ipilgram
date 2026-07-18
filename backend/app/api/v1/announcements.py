import logging
import math
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.core.database import get_db
from app.api.deps import require_role, get_current_user
from app.models.user import User, Role
from app.models.announcement import Announcement, TargetType, AnnouncementPriority
from app.models.package import Package
from app.models.flight import Flight
from app.models.accommodation import Accommodation
from app.models.transport import Transport
from app.schemas.common import PaginationParams, SortingParams, paginate
from app.schemas.announcement import (
    AnnouncementCreate,
    AnnouncementResponse,
    AnnouncementUpdate,
    PaginatedAnnouncements,
)

logger = logging.getLogger("hajj_api")

router = APIRouter(prefix="/announcements", tags=["Announcements"])

ALLOWED_SORT_FIELDS = ["id", "title", "priority", "target_type", "publish_date", "expiry_date", "created_at"]


def _validate_target(target_type: TargetType, target_id: int | None, db: Session):
    if target_type == TargetType.all:
        return
    if target_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"target_id required for target_type '{target_type.value}'",
        )
    validators = {
        TargetType.pilgrim: (User, User.id == target_id, User.role == Role.pilgrim),
        TargetType.package: (Package, Package.id == target_id, None),
        TargetType.flight: (Flight, Flight.id == target_id, None),
        TargetType.accommodation: (Accommodation, Accommodation.id == target_id, None),
        TargetType.transport: (Transport, Transport.id == target_id, None),
    }
    model, id_filter, extra = validators[target_type]
    query = db.query(model).filter(id_filter)
    if extra is not None:
        query = query.filter(extra)
    if not query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target {target_type.value} not found",
        )


@router.get(
    "/my",
    response_model=list[AnnouncementResponse],
    summary="Get announcements for authenticated pilgrim",
    description="Returns announcements that match the pilgrim's profile: ALL announcements, or those targeting their pilgrim ID, package, flight, accommodation, or transport.",
    responses={
        200: {"description": "List of matching announcements"},
        401: {"description": "Authentication required"},
    },
)
def get_my_announcements(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    now = datetime.now(timezone.utc)
    base_query = db.query(Announcement).filter(
        Announcement.publish_date <= now,
        Announcement.expiry_date >= now,
    )

    conditions = [Announcement.target_type == TargetType.all]

    if current_user.package_id:
        pkg = db.query(Package).filter(Package.id == current_user.package_id).first()
        if pkg:
            conditions.append(
                and_(Announcement.target_type == TargetType.package, Announcement.target_id == pkg.id)
            )
            if pkg.flight_id:
                conditions.append(
                    and_(Announcement.target_type == TargetType.flight, Announcement.target_id == pkg.flight_id)
                )
            if pkg.accommodation_id:
                conditions.append(
                    and_(Announcement.target_type == TargetType.accommodation, Announcement.target_id == pkg.accommodation_id)
                )
            if pkg.transport_id:
                conditions.append(
                    and_(Announcement.target_type == TargetType.transport, Announcement.target_id == pkg.transport_id)
                )

    conditions.append(
        and_(Announcement.target_type == TargetType.pilgrim, Announcement.target_id == current_user.id)
    )

    items = base_query.filter(or_(*conditions)).order_by(Announcement.created_at.desc()).all()
    return [AnnouncementResponse.model_validate(a) for a in items]


@router.get(
    "",
    response_model=PaginatedAnnouncements,
    summary="List all announcements (admin)",
    description="Retrieve a paginated list of announcements. Supports search, sorting, and filtering by priority and target type.",
    responses={
        200: {"description": "Paginated list of announcements"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def list_announcements(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    pagination: Annotated[PaginationParams, Depends()],
    sorting: Annotated[SortingParams, Depends()],
    search: str = Query("", max_length=255, description="Search across title and message"),
    priority: AnnouncementPriority | None = Query(None, description="Filter by priority level"),
    target_type: TargetType | None = Query(None, description="Filter by target type"),
):
    query = db.query(Announcement)

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Announcement.title.ilike(pattern),
                Announcement.message.ilike(pattern),
            )
        )

    if priority:
        query = query.filter(Announcement.priority == priority)

    if target_type:
        query = query.filter(Announcement.target_type == target_type)

    query = sorting.apply(query, Announcement, ALLOWED_SORT_FIELDS)
    result = paginate(query, pagination)

    return PaginatedAnnouncements(
        items=[AnnouncementResponse.model_validate(a) for a in result["items"]],
        total=result["total"],
        page=result["page"],
        size=result["size"],
        pages=result["pages"],
    )


@router.get(
    "/active",
    response_model=list[AnnouncementResponse],
    summary="Get currently active announcements",
    description="Return announcements that are currently published and not expired. Useful for dashboard widgets.",
    responses={
        200: {"description": "List of active announcements"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def get_active_announcements(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    now = datetime.now(timezone.utc)
    items = (
        db.query(Announcement)
        .filter(Announcement.publish_date <= now, Announcement.expiry_date >= now)
        .order_by(Announcement.created_at.desc())
        .limit(10)
        .all()
    )
    return [AnnouncementResponse.model_validate(a) for a in items]


@router.get(
    "/{announcement_id}",
    response_model=AnnouncementResponse,
    summary="Get announcement by ID",
    description="Retrieve a single announcement record.",
    responses={
        200: {"description": "Announcement record"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Announcement not found"},
    },
)
def get_announcement(
    announcement_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    a = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not a:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found"
        )
    return AnnouncementResponse.model_validate(a)


@router.post(
    "",
    response_model=AnnouncementResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new announcement",
    description="Publish a new announcement with targeting. Validates expiry date and target entity existence.",
    responses={
        201: {"description": "Announcement created successfully"},
        400: {"description": "Validation error"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def create_announcement(
    body: AnnouncementCreate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    if body.expiry_date <= body.publish_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expiry date must be after publish date",
        )

    _validate_target(body.target_type, body.target_id, db)

    a = Announcement(**body.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return AnnouncementResponse.model_validate(a)


@router.put(
    "/{announcement_id}",
    response_model=AnnouncementResponse,
    summary="Update an announcement",
    description="Update an existing announcement. Only provided fields are modified.",
    responses={
        200: {"description": "Announcement updated successfully"},
        400: {"description": "Validation error"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Announcement not found"},
    },
)
def update_announcement(
    announcement_id: int,
    body: AnnouncementUpdate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    a = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not a:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found"
        )

    update_data = body.model_dump(exclude_unset=True)

    new_type = update_data.get("target_type", a.target_type)
    new_id = update_data.get("target_id", a.target_id)

    if "target_type" in update_data and update_data["target_type"] == TargetType.all:
        update_data["target_id"] = None
        new_id = None

    if new_type != TargetType.all and new_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"target_id required for target_type '{new_type.value}'",
        )

    pub = update_data.get("publish_date", a.publish_date)
    exp = update_data.get("expiry_date", a.expiry_date)
    if pub and exp and exp <= pub:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expiry date must be after publish date",
        )

    _validate_target(new_type, new_id, db)

    for field, value in update_data.items():
        setattr(a, field, value)

    db.commit()
    db.refresh(a)
    return AnnouncementResponse.model_validate(a)


@router.delete(
    "/{announcement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an announcement",
    description="Permanently remove an announcement record.",
    responses={
        204: {"description": "Announcement deleted"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Announcement not found"},
    },
)
def delete_announcement(
    announcement_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    a = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not a:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found"
        )
    db.delete(a)
    db.commit()
