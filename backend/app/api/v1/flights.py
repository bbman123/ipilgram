from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import require_role
from app.models.user import User, Role
from app.models.flight import Flight, FlightStatus
from app.schemas.common import PaginationParams, SortingParams, paginate
from app.schemas.flight import (
    FlightCreate,
    FlightResponse,
    FlightUpdate,
    PaginatedFlights,
)

router = APIRouter(prefix="/flights", tags=["Flights"])

ALLOWED_SORT_FIELDS = ["id", "airline", "flight_number", "departure_datetime", "arrival_datetime", "status"]


@router.get(
    "",
    response_model=PaginatedFlights,
    summary="List all flights",
    description="Retrieve a paginated list of flights. Supports search, sorting, and filtering by status.",
    responses={
        200: {"description": "Paginated list of flights"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def list_flights(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    pagination: Annotated[PaginationParams, Depends()],
    sorting: Annotated[SortingParams, Depends()],
    search: str = Query("", max_length=255, description="Search across airline, flight number, airports"),
    status_filter: FlightStatus | None = Query(None, alias="status", description="Filter by flight status"),
):
    query = db.query(Flight)

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Flight.airline.ilike(pattern),
                Flight.flight_number.ilike(pattern),
                Flight.departure_airport.ilike(pattern),
                Flight.arrival_airport.ilike(pattern),
            )
        )

    if status_filter:
        query = query.filter(Flight.status == status_filter)

    query = sorting.apply(query, Flight, ALLOWED_SORT_FIELDS)
    result = paginate(query, pagination)

    return PaginatedFlights(
        items=[FlightResponse.model_validate(f) for f in result["items"]],
        total=result["total"],
        page=result["page"],
        size=result["size"],
        pages=result["pages"],
    )


@router.get(
    "/{flight_id}",
    response_model=FlightResponse,
    summary="Get flight by ID",
    description="Retrieve a single flight record.",
    responses={
        200: {"description": "Flight record"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Flight not found"},
    },
)
def get_flight(
    flight_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found"
        )
    return FlightResponse.model_validate(flight)


@router.post(
    "",
    response_model=FlightResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new flight",
    description="Register a new flight record. Validates that arrival is after departure.",
    responses={
        201: {"description": "Flight created successfully"},
        400: {"description": "Arrival must be after departure"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
    },
)
def create_flight(
    body: FlightCreate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    if body.arrival_datetime <= body.departure_datetime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arrival must be after departure",
        )

    flight = Flight(**body.model_dump())
    db.add(flight)
    db.commit()
    db.refresh(flight)
    return FlightResponse.model_validate(flight)


@router.put(
    "/{flight_id}",
    response_model=FlightResponse,
    summary="Update flight details",
    description="Update an existing flight record. Only provided fields are modified.",
    responses={
        200: {"description": "Flight updated successfully"},
        400: {"description": "Arrival must be after departure"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Flight not found"},
    },
)
def update_flight(
    flight_id: int,
    body: FlightUpdate,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found"
        )

    update_data = body.model_dump(exclude_unset=True)

    dep = update_data.get("departure_datetime", flight.departure_datetime)
    arr = update_data.get("arrival_datetime", flight.arrival_datetime)
    if dep and arr and arr <= dep:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arrival must be after departure",
        )

    for field, value in update_data.items():
        setattr(flight, field, value)

    db.commit()
    db.refresh(flight)
    return FlightResponse.model_validate(flight)


@router.delete(
    "/{flight_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a flight",
    description="Permanently remove a flight record.",
    responses={
        204: {"description": "Flight deleted"},
        401: {"description": "Authentication required"},
        403: {"description": "Admin role required"},
        404: {"description": "Flight not found"},
    },
)
def delete_flight(
    flight_id: int,
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Flight not found"
        )
    db.delete(flight)
    db.commit()
