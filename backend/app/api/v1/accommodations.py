import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.api.deps import require_role
from app.models.user import User, Role
from app.models.accommodation import Accommodation
from app.schemas.accommodation import (
    AccommodationCreate,
    AccommodationResponse,
    AccommodationUpdate,
    AccommodationWithPilgrim,
    PaginatedAccommodations,
)

router = APIRouter(prefix="/accommodations", tags=["Accommodations"])


def _with_pilgrim(acc: Accommodation, db: Session) -> AccommodationWithPilgrim:
    pilgrim = db.query(User).filter(User.id == acc.pilgrim_id).first()
    return AccommodationWithPilgrim(
        id=acc.id,
        pilgrim_id=acc.pilgrim_id,
        hotel_name=acc.hotel_name,
        city=acc.city,
        building=acc.building,
        floor=acc.floor,
        room_number=acc.room_number,
        bed_number=acc.bed_number,
        address=acc.address,
        check_in=acc.check_in,
        check_out=acc.check_out,
        created_at=str(acc.created_at),
        updated_at=str(acc.updated_at),
        pilgrim_name=pilgrim.full_name if pilgrim else None,
        pilgrim_email=pilgrim.email if pilgrim else None,
    )


@router.get("", response_model=PaginatedAccommodations)
def list_accommodations(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str = Query("", max_length=255),
    pilgrim_id: int | None = Query(None),
    city: str | None = Query(None),
):
    query = db.query(Accommodation)

    if search:
        pattern = f"%{search}%"
        query = query.join(User, Accommodation.pilgrim_id == User.id, isouter=True).filter(
            or_(
                Accommodation.hotel_name.ilike(pattern),
                Accommodation.city.ilike(pattern),
                Accommodation.room_number.ilike(pattern),
                User.full_name.ilike(pattern),
                User.email.ilike(pattern),
            )
        )

    if pilgrim_id:
        query = query.filter(Accommodation.pilgrim_id == pilgrim_id)

    if city:
        query = query.filter(Accommodation.city.ilike(f"%{city}%"))

    total = query.count()
    pages = math.ceil(total / size) if total > 0 else 1
    items = (
        query.order_by(Accommodation.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return PaginatedAccommodations(
        items=[_with_pilgrim(a, db) for a in items],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get("/{accommodation_id}", response_model=AccommodationWithPilgrim)
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
    return _with_pilgrim(acc, db)


@router.post("", response_model=AccommodationWithPilgrim, status_code=status.HTTP_201_CREATED)
def create_accommodation(
    body: AccommodationCreate,
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

    if body.check_out <= body.check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out must be after check-in",
        )

    acc = Accommodation(**body.model_dump())
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return _with_pilgrim(acc, db)


@router.put("/{accommodation_id}", response_model=AccommodationWithPilgrim)
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

    if "pilgrim_id" in update_data:
        pilgrim = (
            db.query(User)
            .filter(User.id == update_data["pilgrim_id"], User.role == Role.pilgrim)
            .first()
        )
        if not pilgrim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pilgrim not found"
            )

    for field, value in update_data.items():
        setattr(acc, field, value)

    ci = acc.check_in
    co = acc.check_out
    if ci and co and co <= ci:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out must be after check-in",
        )

    db.commit()
    db.refresh(acc)
    return _with_pilgrim(acc, db)


@router.delete("/{accommodation_id}", status_code=status.HTTP_204_NO_CONTENT)
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
