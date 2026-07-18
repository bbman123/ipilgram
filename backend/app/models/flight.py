import enum

from sqlalchemy import String, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class FlightStatus(str, enum.Enum):
    scheduled = "scheduled"
    confirmed = "confirmed"
    boarding = "boarding"
    departed = "departed"
    in_air = "in_air"
    landed = "landed"
    cancelled = "cancelled"
    delayed = "delayed"


class Flight(Base):
    __tablename__ = "flights"

    id: Mapped[int] = mapped_column(primary_key=True)
    pilgrim_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    airline: Mapped[str] = mapped_column(String(255))
    flight_number: Mapped[str] = mapped_column(String(50))
    departure_airport: Mapped[str] = mapped_column(String(100))
    arrival_airport: Mapped[str] = mapped_column(String(100))
    departure_datetime: Mapped[str] = mapped_column(DateTime)
    arrival_datetime: Mapped[str] = mapped_column(DateTime)
    gate: Mapped[str | None] = mapped_column(String(20), nullable=True)
    seat_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    status: Mapped[FlightStatus] = mapped_column(
        Enum(FlightStatus), default=FlightStatus.scheduled
    )
    created_at: Mapped[str] = mapped_column(server_default=func.now())
    updated_at: Mapped[str] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
