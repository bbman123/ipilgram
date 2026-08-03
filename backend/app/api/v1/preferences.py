from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import require_role, get_current_user
from app.models.user import User, Role
from app.models.preference import Preference, DELIVERY_MODE_CANONICAL, DeliveryMode
from app.schemas.common import PaginationParams, SortingParams, paginate
from app.schemas.response import success_response
from app.schemas.preference import (
    PreferenceCreate,
    PreferenceResponse,
    PreferenceUpdate,
    PreferenceWithPilgrim,
    PaginatedPreferences,
)

router = APIRouter(prefix="/preferences", tags=["Preferences"])

ALLOWED_SORT_FIELDS = ["id", "preferred_language", "delivery_mode", "font_size", "created_at"]


def _enrich_pref(pref: Preference, pilgrim: User | None) -> PreferenceWithPilgrim:
    return PreferenceWithPilgrim(
        id=pref.id,
        pilgrim_id=pref.pilgrim_id,
        preferred_language=pref.preferred_language,
        delivery_mode=pref.delivery_mode,
        font_size=pref.font_size,
        notifications_enabled=pref.notifications_enabled,
        created_at=pref.created_at,
        updated_at=pref.updated_at,
        pilgrim_name=pilgrim.full_name if pilgrim else None,
        pilgrim_email=pilgrim.email if pilgrim else None,
    )


# ---------------------------------------------------------------------------
# Pilgrim self-service endpoints (MUST be before /{preference_id})
# ---------------------------------------------------------------------------


@router.get(
    "/me",
    summary="Get my preferences",
    description="Pilgrims can retrieve their own preferences.",
    responses={
        200: {"description": "Preference record"},
        401: {"description": "Authentication required"},
    },
)
def get_my_preferences(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    pref = db.query(Preference).filter(Preference.pilgrim_id == current_user.id).first()
    if not pref:
        return success_response(
            data={
                "id": 0,
                "pilgrim_id": current_user.id,
                "preferred_language": "English",
                "delivery_mode": "Text",
                "font_size": 16,
                "notifications_enabled": True,
                "pilgrim_name": current_user.full_name,
                "pilgrim_email": current_user.email,
            },
            message="Using default preferences",
        )
    return success_response(data=_enrich_pref(pref, current_user).model_dump(), message="Preferences retrieved successfully")


@router.put(
    "/me",
    summary="Update my preferences",
    description="Pilgrims can update their own language and notification preferences.",
    responses={
        200: {"description": "Preference updated successfully"},
        401: {"description": "Authentication required"},
    },
)
def update_my_preferences(
    body: PreferenceUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    pref = db.query(Preference).filter(Preference.pilgrim_id == current_user.id).first()
    if not pref:
        pref = Preference(
            pilgrim_id=current_user.id,
            preferred_language=body.preferred_language or "English",
            delivery_mode=body.delivery_mode or "Text",
            font_size=body.font_size or 16,
            notifications_enabled=body.notifications_enabled if body.notifications_enabled is not None else True,
        )
        db.add(pref)
    else:
        update_data = body.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(pref, field, value)
    db.commit()
    db.refresh(pref)
    return success_response(data=_enrich_pref(pref, current_user).model_dump(), message="Preferences updated successfully")


# ---------------------------------------------------------------------------
# Admin endpoints
# ---------------------------------------------------------------------------


@router.get(
    "",
    summary="List all preferences",
    description="Retrieve a paginated list of pilgrim preferences. Supports search, sorting, and filtering by language and delivery mode.",
    responses={
        200: {"description": "Paginated list of preferences"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def list_preferences(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    pagination: Annotated[PaginationParams, Depends()],
    sorting: Annotated[SortingParams, Depends()],
    search: str = Query("", max_length=255, description="Search by pilgrim name or email"),
    pilgrim_id: int | None = Query(None, description="Filter by pilgrim ID"),
    language: str | None = Query(None, description="Filter by preferred language"),
    delivery_mode: str | None = Query(None, description="Filter by delivery mode (Text, Audio, or TextPlusAudio)"),
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
        # Normalize legacy display labels to canonical enum values
        normalized = DELIVERY_MODE_CANONICAL.get(delivery_mode.strip())
        if normalized:
            query = query.filter(Preference.delivery_mode == normalized)
        else:
            # Try direct match (might already be canonical)
            query = query.filter(Preference.delivery_mode == delivery_mode)

    query = sorting.apply(query, Preference, ALLOWED_SORT_FIELDS)
    result = paginate(query, pagination)

    pilgrim_ids = [p.pilgrim_id for p in result["items"]]
    pilgrims = {}
    if pilgrim_ids:
        users = db.query(User).filter(User.id.in_(pilgrim_ids)).all()
        pilgrims = {u.id: u for u in users}

    return success_response(
        data=PaginatedPreferences(
            items=[_enrich_pref(p, pilgrims.get(p.pilgrim_id)) for p in result["items"]],
            total=result["total"],
            page=result["page"],
            size=result["size"],
            pages=result["pages"],
        ).model_dump(),
        message="Preferences retrieved successfully",
    )


@router.get(
    "/by-pilgrim/{pilgrim_id}",
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
    pilgrim = db.query(User).filter(User.id == pref.pilgrim_id).first()
    return success_response(data=_enrich_pref(pref, pilgrim).model_dump(), message="Preference retrieved successfully")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create pilgrim preferences",
    description="Set display and notification preferences for a pilgrim. Each pilgrim can only have one preference record.",
    responses={
        201: {"description": "Preference created successfully"},
        400: {"description": "Preference already exists for this pilgrim"},
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

    pref = Preference(**body.model_dump())
    db.add(pref)
    db.commit()
    db.refresh(pref)
    return success_response(data=_enrich_pref(pref, pilgrim).model_dump(), message="Preference created successfully")


@router.put(
    "/{preference_id}",
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

    for field, value in update_data.items():
        setattr(pref, field, value)

    db.commit()
    db.refresh(pref)
    pilgrim = db.query(User).filter(User.id == pref.pilgrim_id).first()
    return success_response(data=_enrich_pref(pref, pilgrim).model_dump(), message="Preference updated successfully")


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


@router.get(
    "/{preference_id}",
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
    pilgrim = db.query(User).filter(User.id == pref.pilgrim_id).first()
    return success_response(data=_enrich_pref(pref, pilgrim).model_dump(), message="Preference retrieved successfully")
