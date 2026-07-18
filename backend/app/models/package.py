from datetime import datetime

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class Package(Base):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    flight_id: Mapped[int | None] = mapped_column(ForeignKey("flights.id", ondelete="SET NULL"), nullable=True)
    accommodation_id: Mapped[int | None] = mapped_column(ForeignKey("accommodations.id", ondelete="SET NULL"), nullable=True)
    transport_id: Mapped[int | None] = mapped_column(ForeignKey("transports.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
