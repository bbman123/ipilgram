import enum
from datetime import datetime

from sqlalchemy import String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class TransportType(str, enum.Enum):
    bus = "bus"
    van = "van"
    taxi = "taxi"
    car = "car"
    other = "other"


class Transport(Base):
    __tablename__ = "transports"

    id: Mapped[int] = mapped_column(primary_key=True)
    bus_number: Mapped[str] = mapped_column(String(50))
    pickup_location: Mapped[str] = mapped_column(String(255))
    destination: Mapped[str] = mapped_column(String(255))
    pickup_time: Mapped[datetime] = mapped_column(DateTime)
    driver_name: Mapped[str] = mapped_column(String(255))
    driver_phone: Mapped[str] = mapped_column(String(50))
    transport_type: Mapped[TransportType] = mapped_column(
        Enum(TransportType), default=TransportType.bus
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
