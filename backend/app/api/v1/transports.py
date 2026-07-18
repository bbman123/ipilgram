import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.api.deps import require_role
from app.models.user import User, Role
from app.models.transport import Transport, TransportType
from app.schemas.transport import (
    TransportCreate,
    TransportResponse,
    TransportUpdate,
    TransportWithPilgrim,
    PaginatedTransports,
)

router = APIRouter(prefix="/transports", tags=["Transports"])


def _with_pilgrim(t: Transport, db: Session) -> TransportWithPilgrim:
    pilgrim = db.query(User).filter(User.id == t.pilgrim_id).first()
    return TransportWithPilgrim(
        id=t.id,
        pilgrim_id=t.pilgrim_id,
        bus_number=t.bus_number,
        pickup_location=t.pickup_location,
        destination=t.destination,
        pickup_time=t.pickup_time,
        driver_name=t.driver_name,
        driver_phone=t.driver_phone,
        transport_type=t.transport_type,
        created_at=str(t.created_at),
        updated_at=str(t.updated_at),
        pilgrim_name=pilgrim.full_name if pilgrim else None,
        pilgrim_email=pilgrim.email if pilgrim else None,
    )


@router.get(
    "",
    response_model=PaginatedTransports,
    summary="List all transports",
    description="Retrieve a paginated list of transport assignments. Supports search and filtering by type and pilgrim.",
    responses={
        200: {"description": "Paginated list of transports"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def list_transports(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    size: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    search: str = Query("", max_length=255, description="Search across vehicle number, locations, driver, pilgrim name/email"),
    pilgrim_id: int | None = Query(None, description="Filter by assigned pilgrim ID"),
    transport_type: TransportType | None = Query(None, alias="type", description="Filter by transport type"),
):
    query = db.query(Transport)

    if search:
        pattern = f"%{search}%"
        query = query.join(User, Transport.pilgrim_id == User.id, isouter=True).filter(
            or_(
                Transport.bus_number.ilike(pattern),
                Transport.pickup_location.ilike(pattern),
                Transport.destination.ilike(pattern),
                Transport.driver_name.ilike(pattern),
                User.full_name.ilike(pattern),
                User.email.ilike(pattern),
            )
        )

    if pilgrim_id:
        query = query.filter(Transport.pilgrim_id == pilgrim_id)

    if transport_type:
        query = query.filter(Transport.transport_type == transport_type)

    total = query.count()
    pages = math.ceil(total / size) if total > 0 else 1
    items = (
        query.order_by(Transport.pickup_time.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return PaginatedTransports(
        items=[_with_pilgrim(t, db) for t in items],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get(
    "/{transport_id}",
    response_model=TransportWithPilgrim,
    summary="Get transport by ID",
    description="Retrieve a single transport record with pilgrim details.",
    responses={
        200: {"description": "Transport record with pilgrim info"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Transport not found"},
    },
)
def get_transport(
    transport_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    t = db.query(Transport).filter(Transport.id == transport_id).first()
    if not t:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transport not found"
        )
    return _with_pilgrim(t, db)


@router.post(
    "",
    response_model=TransportWithPilgrim,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new transport assignment",
    description="Register a new ground transport assignment for a pilgrim.",
    responses={
        201: {"description": "Transport created successfully"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Pilgrim not found"},
    },
)
def create_transport(
    body: TransportCreate,
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

    t = Transport(**body.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return _with_pilgrim(t, db)


@router.put(
    "/{transport_id}",
    response_model=TransportWithPilgrim,
    summary="Update transport details",
    description="Update an existing transport record. Only provided fields are modified.",
    responses={
        200: {"description": "Transport updated successfully"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Transport or pilgrim not found"},
    },
)
def update_transport(
    transport_id: int,
    body: TransportUpdate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    t = db.query(Transport).filter(Transport.id == transport_id).first()
    if not t:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transport not found"
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
        setattr(t, field, value)

    db.commit()
    db.refresh(t)
    return _with_pilgrim(t, db)


@router.delete(
    "/{transport_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a transport",
    description="Permanently remove a transport record.",
    responses={
        204: {"description": "Transport deleted"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Transport not found"},
    },
)
def delete_transport(
    transport_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    t = db.query(Transport).filter(Transport.id == transport_id).first()
    if not t:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transport not found"
        )
    db.delete(t)
    db.commit()
