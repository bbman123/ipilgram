import logging
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
from app.schemas.response import success_response
from app.schemas.announcement import (
    AnnouncementCreate,
    AnnouncementResponse,
    AnnouncementUpdate,
    PaginatedAnnouncements,
    PersonalizedAnnouncement,
    AVAILABLE_PLACEHOLDERS,
)
from app.services.template_engine import build_replacement_map, replace_placeholders

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


def _get_matching_pilgrim_ids(announcement: Announcement, db: Session) -> list[int]:
    """Resolve which pilgrim IDs match this announcement's targeting."""
    if announcement.target_type == TargetType.all:
        return [
            p.id for p in
            db.query(User.id).filter(User.role == Role.pilgrim, User.is_active == True).all()
        ]

    if announcement.target_type == TargetType.pilgrim:
        return [announcement.target_id] if announcement.target_id else []

    if announcement.target_type == TargetType.package:
        if not announcement.target_id:
            return []
        return [
            u.id for u in
            db.query(User.id).filter(
                User.role == Role.pilgrim,
                User.is_active == True,
                User.package_id == announcement.target_id,
            ).all()
        ]

    if announcement.target_type == TargetType.flight:
        if not announcement.target_id:
            return []
        package_ids = [
            p.id for p in
            db.query(Package.id).filter(Package.flight_id == announcement.target_id).all()
        ]
        if not package_ids:
            return []
        return [
            u.id for u in
            db.query(User.id).filter(
                User.role == Role.pilgrim,
                User.is_active == True,
                User.package_id.in_(package_ids),
            ).all()
        ]

    if announcement.target_type == TargetType.accommodation:
        if not announcement.target_id:
            return []
        package_ids = [
            p.id for p in
            db.query(Package.id).filter(Package.accommodation_id == announcement.target_id).all()
        ]
        if not package_ids:
            return []
        return [
            u.id for u in
            db.query(User.id).filter(
                User.role == Role.pilgrim,
                User.is_active == True,
                User.package_id.in_(package_ids),
            ).all()
        ]

    if announcement.target_type == TargetType.transport:
        if not announcement.target_id:
            return []
        package_ids = [
            p.id for p in
            db.query(Package.id).filter(Package.transport_id == announcement.target_id).all()
        ]
        if not package_ids:
            return []
        return [
            u.id for u in
            db.query(User.id).filter(
                User.role == Role.pilgrim,
                User.is_active == True,
                User.package_id.in_(package_ids),
            ).all()
        ]

    return []


@router.get(
    "",
    summary="List all announcement templates",
    description="Admin endpoint. Retrieve a paginated list of announcement templates. Supports search and filtering.",
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
    search: str = Query("", max_length=255, description="Search by title or message"),
    priority: AnnouncementPriority | None = Query(None, description="Filter by priority"),
    target_type: TargetType | None = Query(None, description="Filter by target type"),
):
    query = db.query(Announcement)

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Announcement.title.ilike(pattern),
                Announcement.message_template.ilike(pattern),
            )
        )
    if priority:
        query = query.filter(Announcement.priority == priority)
    if target_type:
        query = query.filter(Announcement.target_type == target_type)

    query = sorting.apply(query, Announcement, ALLOWED_SORT_FIELDS)
    result = paginate(query, pagination)

    return success_response(
        data=PaginatedAnnouncements(
            items=[AnnouncementResponse.model_validate(a) for a in result["items"]],
            total=result["total"],
            page=result["page"],
            size=result["size"],
            pages=result["pages"],
        ).model_dump(),
        message="Announcements retrieved successfully",
    )


@router.get(
    "/my",
    summary="Get personalized announcements for authenticated pilgrim",
    description=(
        "Pilgrim endpoint. Returns announcements matching the pilgrim's targeting with "
        "placeholders replaced by their actual flight, accommodation, and transport data."
    ),
    responses={
        200: {"description": "List of personalized announcements"},
        401: {"description": "Authentication required"},
        403: {"description": "Pilgrim role required"},
    },
)
def get_my_announcements(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role(Role.pilgrim))],
):
    now = datetime.now(timezone.utc)
    base_conditions = [
        Announcement.publish_date <= now,
        Announcement.expiry_date >= now,
    ]

    target_conditions = [
        Announcement.target_type == TargetType.all,
    ]

    if current_user.package_id:
        target_conditions.append(
            and_(Announcement.target_type == TargetType.package, Announcement.target_id == current_user.package_id)
        )
    target_conditions.append(
        and_(Announcement.target_type == TargetType.pilgrim, Announcement.target_id == current_user.id)
    )

    if current_user.package_id:
        pkg = db.query(Package).filter(Package.id == current_user.package_id).first()
        if pkg:
            if pkg.flight_id:
                target_conditions.append(
                    and_(Announcement.target_type == TargetType.flight, Announcement.target_id == pkg.flight_id)
                )
            if pkg.accommodation_id:
                target_conditions.append(
                    and_(Announcement.target_type == TargetType.accommodation, Announcement.target_id == pkg.accommodation_id)
                )
            if pkg.transport_id:
                target_conditions.append(
                    and_(Announcement.target_type == TargetType.transport, Announcement.target_id == pkg.transport_id)
                )

    announcements = (
        db.query(Announcement)
        .filter(and_(*base_conditions, or_(*target_conditions)))
        .order_by(
            Announcement.priority.desc(),
            Announcement.created_at.desc(),
        )
        .limit(50)
        .all()
    )

    replacements = build_replacement_map(current_user.id, db)

    personalized = []
    for a in announcements:
        personalized_message = replace_placeholders(a.message_template, replacements)
        personalized.append(
            PersonalizedAnnouncement(
                id=a.id,
                title=a.title,
                message=personalized_message,
                priority=a.priority,
                publish_date=a.publish_date,
                expiry_date=a.expiry_date,
                language=replacements.get("language", "English"),
            )
        )

    return success_response(data=[pa.model_dump() for pa in personalized], message="Personalized announcements retrieved successfully")


@router.get(
    "/templates/placeholders",
    summary="List available placeholders",
    description="Returns the list of supported template placeholders that can be used in announcement message templates.",
    responses={
        200: {"description": "List of available placeholders"},
    },
)
def list_placeholders():
    return success_response(data={"placeholders": AVAILABLE_PLACEHOLDERS}, message="Placeholders retrieved successfully")


@router.get(
    "/active",
    summary="Get currently active announcements",
    description="Public-ish endpoint. Returns all announcements within their publish/expiry window.",
    responses={
        200: {"description": "List of active announcements"},
    },
)
def get_active_announcements(
    db: Annotated[Session, Depends(get_db)],
):
    now = datetime.now(timezone.utc)
    announcements = (
        db.query(Announcement)
        .filter(
            Announcement.publish_date <= now,
            Announcement.expiry_date >= now,
        )
        .order_by(Announcement.created_at.desc())
        .all()
    )
    return success_response(data=[AnnouncementResponse.model_validate(a).model_dump() for a in announcements], message="Active announcements retrieved successfully")


@router.get(
    "/{announcement_id}",
    summary="Get announcement by ID",
    description="Retrieve a single announcement template by its unique identifier.",
    responses={
        200: {"description": "Announcement details"},
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found")
    return success_response(data=AnnouncementResponse.model_validate(a).model_dump(), message="Announcement retrieved successfully")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create announcement template",
    description=(
        "Create a new announcement template. Supports placeholders like "
        "{{pilgrim_name}}, {{flight_number}}, {{departure_time}}, etc."
    ),
    responses={
        201: {"description": "Announcement created"},
        400: {"description": "Invalid target_id for target_type"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def create_announcement(
    body: AnnouncementCreate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    _validate_target(body.target_type, body.target_id, db)

    a = Announcement(**body.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return success_response(data=AnnouncementResponse.model_validate(a).model_dump(), message="Announcement created successfully")


@router.put(
    "/{announcement_id}",
    summary="Update announcement template",
    description="Update an existing announcement template. Only provided fields are modified.",
    responses={
        200: {"description": "Announcement updated"},
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found")

    update_data = body.model_dump(exclude_unset=True)

    if "target_type" in update_data:
        target_type = update_data["target_type"]
        target_id = update_data.get("target_id", a.target_id)
        if target_type is not None and target_type != TargetType.all and target_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"target_id required for target_type '{target_type.value}'",
            )
        if target_type == TargetType.all:
            update_data["target_id"] = None

    for field, value in update_data.items():
        setattr(a, field, value)

    db.commit()
    db.refresh(a)
    return success_response(data=AnnouncementResponse.model_validate(a).model_dump(), message="Announcement updated successfully")


@router.delete(
    "/{announcement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete announcement",
    description="Permanently remove an announcement template.",
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Announcement not found")
    db.delete(a)
    db.commit()
