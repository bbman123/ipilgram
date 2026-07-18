import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.api.deps import require_role
from app.core.security import hash_password
from app.models.user import User, Role
from app.schemas.pilgrim import (
    PaginatedPilgrims,
    PilgrimCreate,
    PilgrimResponse,
    PilgrimUpdate,
)

router = APIRouter(prefix="/pilgrims", tags=["Pilgrims"])


@router.get("", response_model=PaginatedPilgrims)
def list_pilgrims(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str = Query("", max_length=255),
):
    query = db.query(User).filter(User.role == Role.pilgrim)

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                User.full_name.ilike(pattern),
                User.email.ilike(pattern),
                User.phone.ilike(pattern),
                User.nationality.ilike(pattern),
                User.passport_number.ilike(pattern),
            )
        )

    total = query.count()
    pages = math.ceil(total / size) if total > 0 else 1
    items = (
        query.order_by(User.id.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return PaginatedPilgrims(
        items=items, total=total, page=page, size=size, pages=pages
    )


@router.get("/{pilgrim_id}", response_model=PilgrimResponse)
def get_pilgrim(
    pilgrim_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    user = (
        db.query(User)
        .filter(User.id == pilgrim_id, User.role == Role.pilgrim)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pilgrim not found"
        )
    return user


@router.post("", response_model=PilgrimResponse, status_code=status.HTTP_201_CREATED)
def create_pilgrim(
    body: PilgrimCreate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    user = User(
        email=body.email,
        full_name=body.full_name,
        hashed_password=hash_password(body.password),
        role=Role.pilgrim,
        phone=body.phone,
        nationality=body.nationality,
        passport_number=body.passport_number,
        emergency_contact=body.emergency_contact,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put("/{pilgrim_id}", response_model=PilgrimResponse)
def update_pilgrim(
    pilgrim_id: int,
    body: PilgrimUpdate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    user = (
        db.query(User)
        .filter(User.id == pilgrim_id, User.role == Role.pilgrim)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pilgrim not found"
        )

    update_data = body.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"] != user.email:
        existing = db.query(User).filter(User.email == update_data["email"]).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{pilgrim_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pilgrim(
    pilgrim_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    user = (
        db.query(User)
        .filter(User.id == pilgrim_id, User.role == Role.pilgrim)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pilgrim not found"
        )
    db.delete(user)
    db.commit()
