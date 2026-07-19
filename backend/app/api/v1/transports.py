from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import require_role
from app.models.user import User, Role
from app.models.transport import Transport, TransportType
from app.schemas.common import PaginationParams, SortingParams, paginate
from app.schemas.response import success_response
from app.schemas.transport import (
    TransportCreate,
    TransportResponse,
    TransportUpdate,
    PaginatedTransports,
)

router = APIRouter(prefix="/transports", tags=["Transports"])

ALLOWED_SORT_FIELDS = ["id", "bus_number", "pickup_location", "destination", "pickup_time", "transport_type"]


@router.get(
    "",
    summary="List all transports",
    description="Retrieve a paginated list of transport records. Supports search, sorting, and filtering by type.",
    responses={
        200: {"description": "Paginated list of transports"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def list_transports(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    pagination: Annotated[PaginationParams, Depends()],
    sorting: Annotated[SortingParams, Depends()],
    search: str = Query("", max_length=255, description="Search across vehicle number, locations, driver"),
    transport_type: TransportType | None = Query(None, alias="type", description="Filter by transport type"),
):
    query = db.query(Transport)

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Transport.bus_number.ilike(pattern),
                Transport.pickup_location.ilike(pattern),
                Transport.destination.ilike(pattern),
                Transport.driver_name.ilike(pattern),
            )
        )

    if transport_type:
        query = query.filter(Transport.transport_type == transport_type)

    query = sorting.apply(query, Transport, ALLOWED_SORT_FIELDS)
    result = paginate(query, pagination)

    return success_response(
        data=PaginatedTransports(
            items=[TransportResponse.model_validate(t) for t in result["items"]],
            total=result["total"],
            page=result["page"],
            size=result["size"],
            pages=result["pages"],
        ).model_dump(),
        message="Transports retrieved successfully",
    )


@router.get(
    "/{transport_id}",
    summary="Get transport by ID",
    description="Retrieve a single transport record.",
    responses={
        200: {"description": "Transport record"},
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
    return success_response(data=TransportResponse.model_validate(t).model_dump(), message="Transport retrieved successfully")


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new transport assignment",
    description="Register a new ground transport record.",
    responses={
        201: {"description": "Transport created successfully"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def create_transport(
    body: TransportCreate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    t = Transport(**body.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    return success_response(data=TransportResponse.model_validate(t).model_dump(), message="Transport created successfully")


@router.put(
    "/{transport_id}",
    summary="Update transport details",
    description="Update an existing transport record. Only provided fields are modified.",
    responses={
        200: {"description": "Transport updated successfully"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Transport not found"},
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
    for field, value in update_data.items():
        setattr(t, field, value)

    db.commit()
    db.refresh(t)
    return success_response(data=TransportResponse.model_validate(t).model_dump(), message="Transport updated successfully")


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
