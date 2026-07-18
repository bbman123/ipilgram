import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.api.deps import require_role
from app.models.user import User, Role
from app.models.flight import Flight, FlightStatus
from app.schemas.flight import (
    FlightCreate,
    FlightResponse,
    FlightUpdate,
    FlightWithPilgrim,
    PaginatedFlights,
)

router = APIRouter(prefix="/flights", tags=["Flights"])


def _flight_with_pilgrim(flight: Flight, db: Session) -> FlightWithPilgrim:
    pilgrim = db.query(User).filter(User.id == flight.pilgrim_id).first()
    return FlightWithPilgrim(
        id=flight.id,
        pilgrim_id=flight.pilgrim_id,
        airline=flight.airline,
        flight_number=flight.flight_number,
        departure_airport=flight.departure_airport,
        arrival_airport=flight.arrival_airport,
        departure_datetime=flight.departure_datetime,
        arrival_datetime=flight.arrival_datetime,
        gate=flight.gate,
        seat_number=flight.seat_number,
        status=flight.status,
        created_at=str(flight.created_at),
        updated_at=str(flight.updated_at),
        pilgrim_name=pilgrim.full_name if pilgrim else None,
        pilgrim_email=pilgrim.email if pilgrim else None,
    )


@router.get("", response_model=PaginatedFlights)
def list_flights(
    db: Annotated[Session, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(Role.admin))],
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str = Query("", max_length=255),
    status_filter: FlightStatus | None = Query(None, alias="status"),
    pilgrim_id: int | None = Query(None),
):
    query = db.query(Flight)

    if search:
        pattern = f"%{search}%"
        query = query.join(User, Flight.pilgrim_id == User.id, isouter=True).filter(
            or_(
                Flight.airline.ilike(pattern),
                Flight.flight_number.ilike(pattern),
                Flight.departure_airport.ilike(pattern),
                Flight.arrival_airport.ilike(pattern),
                User.full_name.ilike(pattern),
                User.email.ilike(pattern),
            )
        )

    if status_filter:
        query = query.filter(Flight.status == status_filter)

    if pilgrim_id:
        query = query.filter(Flight.pilgrim_id == pilgrim_id)

    total = query.count()
    pages = math.ceil(total / size) if total > 0 else 1
    items = (
        query.order_by(Flight.departure_datetime.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )

    return PaginatedFlights(
        items=[_flight_with_pilgrim(f, db) for f in items],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get("/{flight_id}", response_model=FlightWithPilgrim)
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
    return _flight_with_pilgrim(flight, db)


@router.post("", response_model=FlightWithPilgrim, status_code=status.HTTP_201_CREATED)
def create_flight(
    body: FlightCreate,
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

    if body.arrival_datetime <= body.departure_datetime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arrival must be after departure",
        )

    flight = Flight(**body.model_dump())
    db.add(flight)
    db.commit()
    db.refresh(flight)
    return _flight_with_pilgrim(flight, db)


@router.put("/{flight_id}", response_model=FlightWithPilgrim)
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

    if "pilgrim_id" in update_data:
        pilgrim = (
            db.query(User)
            .filter(
                User.id == update_data["pilgrim_id"], User.role == Role.pilgrim
            )
            .first()
        )
        if not pilgrim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Pilgrim not found"
            )

    for field, value in update_data.items():
        setattr(flight, field, value)

    dep = flight.departure_datetime
    arr = flight.arrival_datetime
    if dep and arr and arr <= dep:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arrival must be after departure",
        )

    db.commit()
    db.refresh(flight)
    return _flight_with_pilgrim(flight, db)


@router.delete("/{flight_id}", status_code=status.HTTP_204_NO_CONTENT)
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
