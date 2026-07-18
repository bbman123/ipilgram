import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.api.deps import require_role
from app.models.user import User, Role
from app.models.announcement import (
    Announcement,
    AnnouncementCategory,
    AnnouncementPriority,
)
from app.schemas.announcement import (
    AnnouncementCreate,
    AnnouncementResponse,
    AnnouncementUpdate,
    PaginatedAnnouncements,
)

router = APIRouter(prefix="/announcements", tags=["Announcements"])


@router.get(
    "",
    response_model=PaginatedAnnouncements,
    summary="List all announcements",
    description="Retrieve a paginated list of announcements. Supports search and filtering by category, priority, and language.",
    responses={
        200: {"description": "Paginated list of announcements"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def list_announcements(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    size: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    search: str = Query("", max_length=255, description="Search across title and message"),
    category: AnnouncementCategory | None = Query(None, description="Filter by category"),
    priority: AnnouncementPriority | None = Query(None, description="Filter by priority level"),
    language: str | None = Query(None, description="Filter by language code (e.g. en, ha, ar)"),
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

    if category:
        query = query.filter(Announcement.category == category)

    if priority:
        query = query.filter(Announcement.priority == priority)

    if language:
        query = query.filter(Announcement.language.ilike(language))

    total = query.count()
    pages = math.ceil(total / size) if total > 0 else 1
    items = (
        query.order_by(Announcement.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return PaginatedAnnouncements(
        items=[AnnouncementResponse.model_validate(a) for a in items],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


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
    description="Publish a new announcement. Validates that expiry date is after publish date.",
    responses={
        201: {"description": "Announcement created successfully"},
        400: {"description": "Expiry date must be after publish date"},
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
        400: {"description": "Expiry date must be after publish date"},
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
    for field, value in update_data.items():
        setattr(a, field, value)

    if a.expiry_date and a.publish_date and a.expiry_date <= a.publish_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expiry date must be after publish date",
        )

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
