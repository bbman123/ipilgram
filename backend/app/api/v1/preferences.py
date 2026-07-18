import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.api.deps import require_role
from app.models.user import User, Role
from app.models.preference import Preference
from app.schemas.preference import (
    PreferenceCreate,
    PreferenceResponse,
    PreferenceUpdate,
    PreferenceWithPilgrim,
    PaginatedPreferences,
)

router = APIRouter(prefix="/preferences", tags=["Preferences"])


def _with_pilgrim(pref: Preference, db: Session) -> PreferenceWithPilgrim:
    pilgrim = db.query(User).filter(User.id == pref.pilgrim_id).first()
    return PreferenceWithPilgrim(
        id=pref.id,
        pilgrim_id=pref.pilgrim_id,
        preferred_language=pref.preferred_language,
        delivery_mode=pref.delivery_mode,
        font_size=pref.font_size,
        notifications_enabled=pref.notifications_enabled,
        created_at=str(pref.created_at),
        updated_at=str(pref.updated_at),
        pilgrim_name=pilgrim.full_name if pilgrim else None,
        pilgrim_email=pilgrim.email if pilgrim else None,
    )


@router.get(
    "",
    response_model=PaginatedPreferences,
    summary="List all preferences",
    description="Retrieve a paginated list of pilgrim preferences. Supports search and filtering by language and delivery mode.",
    responses={
        200: {"description": "Paginated list of preferences"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def list_preferences(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    size: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    search: str = Query("", max_length=255, description="Search by pilgrim name or email"),
    pilgrim_id: int | None = Query(None, description="Filter by pilgrim ID"),
    language: str | None = Query(None, description="Filter by preferred language"),
    delivery_mode: str | None = Query(None, alias="delivery_mode", description="Filter by delivery mode"),
):
    query = db.query(Preference)

    if search:
        pattern = f"%{search}%"
        query = query.join(User, Preference.pilgrim_id == User.id, isouter=True).filter(
            or_(
                User.full_name.ilike(pattern),
                User.email.ilike(pattern),
            )
        )

    if pilgrim_id:
        query = query.filter(Preference.pilgrim_id == pilgrim_id)

    if language:
        query = query.filter(Preference.preferred_language == language)

    if delivery_mode:
        query = query.filter(Preference.delivery_mode == delivery_mode)

    total = query.count()
    pages = math.ceil(total / size) if total > 0 else 1
    items = (
        query.order_by(Preference.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return PaginatedPreferences(
        items=[_with_pilgrim(p, db) for p in items],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get(
    "/{preference_id}",
    response_model=PreferenceWithPilgrim,
    summary="Get preference by ID",
    description="Retrieve a single preference record with pilgrim details.",
    responses={
        200: {"description": "Preference record with pilgrim info"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Preference not found"},
    },
)
def get_preference(
    preference_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    pref = db.query(Preference).filter(Preference.id == preference_id).first()
    if not pref:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Preference not found"
        )
    return _with_pilgrim(pref, db)


@router.get(
    "/by-pilgrim/{pilgrim_id}",
    response_model=PreferenceWithPilgrim,
    summary="Get preference by pilgrim ID",
    description="Retrieve preferences for a specific pilgrim by their user ID.",
    responses={
        200: {"description": "Preference record"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Preference not found for this pilgrim"},
    },
)
def get_preference_by_pilgrim(
    pilgrim_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    pref = db.query(Preference).filter(Preference.pilgrim_id == pilgrim_id).first()
    if not pref:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preference not found for this pilgrim",
        )
    return _with_pilgrim(pref, db)


@router.post(
    "",
    response_model=PreferenceWithPilgrim,
    status_code=status.HTTP_201_CREATED,
    summary="Create pilgrim preferences",
    description="Set display and notification preferences for a pilgrim. Each pilgrim can only have one preference record.",
    responses={
        201: {"description": "Preference created successfully"},
        400: {"description": "Preference already exists for this pilgrim, or font size out of range (8-48)"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Pilgrim not found"},
    },
)
def create_preference(
    body: PreferenceCreate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    pilgrim = (
        db.query(User)
        .filter(User.id == body.pilgrim_id, User.role == Role.pilgrim)
        .first()
    )
    if not pilgrim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pilgrim not found"
        )

    existing = (
        db.query(Preference).filter(Preference.pilgrim_id == body.pilgrim_id).first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Preference already exists for this pilgrim. Use PUT to update.",
        )

    if body.font_size < 8 or body.font_size > 48:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Font size must be between 8 and 48",
        )

    pref = Preference(**body.model_dump())
    db.add(pref)
    db.commit()
    db.refresh(pref)
    return _with_pilgrim(pref, db)


@router.put(
    "/{preference_id}",
    response_model=PreferenceWithPilgrim,
    summary="Update pilgrim preferences",
    description="Update an existing preference record. Only provided fields are modified.",
    responses={
        200: {"description": "Preference updated successfully"},
        400: {"description": "Font size must be between 8 and 48"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Preference not found"},
    },
)
def update_preference(
    preference_id: int,
    body: PreferenceUpdate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    pref = db.query(Preference).filter(Preference.id == preference_id).first()
    if not pref:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Preference not found"
        )

    update_data = body.model_dump(exclude_unset=True)

    if "font_size" in update_data:
        fs = update_data["font_size"]
        if fs < 8 or fs > 48:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Font size must be between 8 and 48",
            )

    for field, value in update_data.items():
        setattr(pref, field, value)

    db.commit()
    db.refresh(pref)
    return _with_pilgrim(pref, db)


@router.delete(
    "/{preference_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete preferences",
    description="Permanently remove a preference record for a pilgrim.",
    responses={
        204: {"description": "Preference deleted"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Preference not found"},
    },
)
def delete_preference(
    preference_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    pref = db.query(Preference).filter(Preference.id == preference_id).first()
    if not pref:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Preference not found"
        )
    db.delete(pref)
    db.commit()
