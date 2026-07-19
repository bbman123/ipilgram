from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import require_role
from app.models.user import User, Role
from app.models.accommodation import Accommodation
from app.schemas.common import PaginationParams, SortingParams, paginate
from app.schemas.response import success_response
from app.schemas.accommodation import (
    AccommodationCreate,
    AccommodationResponse,
    AccommodationUpdate,
    PaginatedAccommodations,
)

router = APIRouter(prefix="/accommodations", tags=["Accommodations"])

ALLOWED_SORT_FIELDS = ["id", "hotel_name", "city", "check_in", "check_out", "created_at"]


@router.get(
    "",
    summary="List all accommodations",
    description="Retrieve a paginated list of accommodations. Supports search, sorting, and filtering by city.",
    responses={
        200: {"description": "Paginated list of accommodations"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def list_accommodations(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    pagination: Annotated[PaginationParams, Depends()],
    sorting: Annotated[SortingParams, Depends()],
    search: str = Query("", max_length=255, description="Search across hotel, city, room"),
    city: str | None = Query(None, description="Filter by city name (partial match)"),
):
    query = db.query(Accommodation)

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Accommodation.hotel_name.ilike(pattern),
                Accommodation.city.ilike(pattern),
                Accommodation.room_number.ilike(pattern),
            )
        )

    if city:
        query = query.filter(Accommodation.city.ilike(f"%{city}%"))

    query = sorting.apply(query, Accommodation, ALLOWED_SORT_FIELDS)
    result = paginate(query, pagination)

    return success_response(
        data=PaginatedAccommodations(
            items=[AccommodationResponse.model_validate(a) for a in result["items"]],
            total=result["total"],
            page=result["page"],
            size=result["size"],
            pages=result["pages"],
        ).model_dump(),
        message="Accommodations retrieved successfully",
    )


@router.get(
    "/{accommodation_id}",
    summary="Get accommodation by ID",
    description="Retrieve a single accommodation record.",
    responses={
        200: {"description": "Accommodation record"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Accommodation not found"},
    },
)
def get_accommodation(
    accommodation_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    acc = db.query(Accommodation).filter(Accommodation.id == accommodation_id).first()
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Accommodation not found"
        )
    return success_response(data=AccommodationResponse.model_validate(acc).model_dump(), message="Accommodation retrieved successfully")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new accommodation",
    description="Register a new accommodation record. Validates check-out is after check-in.",
    responses={
        201: {"description": "Accommodation created successfully"},
        400: {"description": "Check-out must be after check-in"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def create_accommodation(
    body: AccommodationCreate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    if body.check_out <= body.check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out must be after check-in",
        )

    acc = Accommodation(**body.model_dump())
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return success_response(data=AccommodationResponse.model_validate(acc).model_dump(), message="Accommodation created successfully")


@router.put(
    "/{accommodation_id}",
    summary="Update accommodation details",
    description="Update an existing accommodation record. Only provided fields are modified.",
    responses={
        200: {"description": "Accommodation updated successfully"},
        400: {"description": "Check-out must be after check-in"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Accommodation not found"},
    },
)
def update_accommodation(
    accommodation_id: int,
    body: AccommodationUpdate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    acc = db.query(Accommodation).filter(Accommodation.id == accommodation_id).first()
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Accommodation not found"
        )

    update_data = body.model_dump(exclude_unset=True)

    ci = update_data.get("check_in", acc.check_in)
    co = update_data.get("check_out", acc.check_out)
    if ci and co and co <= ci:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out must be after check-in",
        )

    for field, value in update_data.items():
        setattr(acc, field, value)

    db.commit()
    db.refresh(acc)
    return success_response(data=AccommodationResponse.model_validate(acc).model_dump(), message="Accommodation updated successfully")


@router.delete(
    "/{accommodation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an accommodation",
    description="Permanently remove an accommodation record.",
    responses={
        204: {"description": "Accommodation deleted"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Accommodation not found"},
    },
)
def delete_accommodation(
    accommodation_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    acc = db.query(Accommodation).filter(Accommodation.id == accommodation_id).first()
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Accommodation not found"
        )
    db.delete(acc)
    db.commit()
