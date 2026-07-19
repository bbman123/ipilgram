from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.api.deps import require_role
from app.core.security import hash_password
from app.models.user import User, Role
from app.models.package import Package
from app.schemas.common import PaginationParams, SortingParams, paginate
from app.schemas.response import success_response
from app.schemas.pilgrim import (
    PaginatedPilgrims,
    PilgrimCreate,
    PilgrimResponse,
    PilgrimUpdate,
)

router = APIRouter(prefix="/pilgrims", tags=["Pilgrims"])

ALLOWED_SORT_FIELDS = ["id", "full_name", "email", "created_at"]


@router.get(
    "",
    summary="List all pilgrims",
    description="Retrieve a paginated list of pilgrims. Supports search, sorting, and pagination.",
    responses={
        200: {"description": "Paginated list of pilgrims"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def list_pilgrims(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    pagination: Annotated[PaginationParams, Depends()],
    sorting: Annotated[SortingParams, Depends()],
    search: str = Query("", max_length=255, description="Search across name, email, phone, nationality, passport"),
    package_id: int | None = Query(None, description="Filter by assigned package ID"),
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

    if package_id is not None:
        query = query.filter(User.package_id == package_id)

    query = sorting.apply(query, User, ALLOWED_SORT_FIELDS)
    result = paginate(query, pagination)

    pkg_ids = {u.package_id for u in result["items"] if u.package_id}
    pkg_names = {}
    if pkg_ids:
        packages = db.query(Package.id, Package.name).filter(Package.id.in_(pkg_ids)).all()
        pkg_names = {p.id: p.name for p in packages}

    items = []
    for u in result["items"]:
        resp = PilgrimResponse.model_validate(u)
        resp.package_name = pkg_names.get(u.package_id)
        items.append(resp)

    return success_response(
        data=PaginatedPilgrims(
            items=items,
            total=result["total"],
            page=result["page"],
            size=result["size"],
            pages=result["pages"],
        ).model_dump(),
        message="Pilgrims retrieved successfully",
    )


@router.get(
    "/{pilgrim_id}",
    summary="Get pilgrim by ID",
    description="Retrieve a single pilgrim's profile by their unique identifier.",
    responses={
        200: {"description": "Pilgrim profile"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Pilgrim not found"},
    },
)
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
    return success_response(data=PilgrimResponse.model_validate(user).model_dump(), message="Pilgrim retrieved successfully")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new pilgrim",
    description="Register a new pilgrim account. Email must be unique across the system.",
    responses={
        201: {"description": "Pilgrim created successfully"},
        400: {"description": "Email already registered"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
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
    return success_response(data=PilgrimResponse.model_validate(user).model_dump(), message="Pilgrim created successfully")


@router.put(
    "/{pilgrim_id}",
    summary="Update pilgrim profile",
    description="Update an existing pilgrim's information. Only provided fields are updated.",
    responses={
        200: {"description": "Pilgrim updated successfully"},
        400: {"description": "Email already registered"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Pilgrim not found"},
    },
)
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
    return success_response(data=PilgrimResponse.model_validate(user).model_dump(), message="Pilgrim updated successfully")


@router.delete(
    "/{pilgrim_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a pilgrim",
    description="Permanently remove a pilgrim account and all associated data (cascade).",
    responses={
        204: {"description": "Pilgrim deleted"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Pilgrim not found"},
    },
)
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
