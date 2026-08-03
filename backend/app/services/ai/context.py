"""Builds a restricted, pilgrim-scoped context for AI processing.

The AI never receives raw database access. This module fetches ONLY the
data the pilgrim is authorized to see, formats it as a structured context,
and passes it to the AI provider.
"""

import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.user import User, Role
from app.models.package import Package
from app.models.flight import Flight
from app.models.accommodation import Accommodation
from app.models.transport import Transport
from app.models.announcement import Announcement, TargetType
from app.models.preference import Preference

logger = logging.getLogger("hajj_api")


class PilgrimContext:
    """Structured context built from a single pilgrim's authorized data."""

    def __init__(
        self,
        pilgrim: User,
        preference: Preference | None,
        package: Package | None,
        flight: Flight | None,
        accommodation: Accommodation | None,
        transport: Transport | None,
        announcements: list[Announcement],
    ):
        self.pilgrim = pilgrim
        self.preference = preference
        self.package = package
        self.flight = flight
        self.accommodation = accommodation
        self.transport = transport
        self.announcements = announcements

    def to_prompt_context(self) -> str:
        """Serialize authorized data into a prompt-ready context string.

        This is the ONLY data the AI provider will see.
        """
        lines = []

        logger.info("Entering to_prompt_context...")

        if self.preference and self.preference.preferred_language:
            logger.info(
                "preference.preferred_language type=%s value=%r",
                type(self.preference.preferred_language).__name__,
                self.preference.preferred_language,
            )
        if self.flight and self.flight.status:
            logger.info(
                "flight.status type=%s value=%r",
                type(self.flight.status).__name__,
                self.flight.status,
            )
        if self.transport and self.transport.transport_type:
            logger.info(
                "transport.transport_type type=%s value=%r",
                type(self.transport.transport_type).__name__,
                self.transport.transport_type,
            )
        if self.announcements:
            for i, a in enumerate(self.announcements[:3]):
                logger.info(
                    "announcement[%d].priority type=%s value=%r",
                    i,
                    type(a.priority).__name__,
                    a.priority,
                )

        if self.preference and self.preference.preferred_language:
            lang = self.preference.preferred_language.value
        else:
            lang = "English"

        lines.append("=== PILGRIM PROFILE ===")
        lines.append(f"Name: {self.pilgrim.full_name}")
        lines.append(f"Language: {lang}")
        if self.pilgrim.nationality:
            lines.append(f"Nationality: {self.pilgrim.nationality}")

        if self.package:
            lines.append("")
            lines.append("=== ASSIGNED PACKAGE ===")
            lines.append(f"Package: {self.package.name}")
            if self.package.description:
                lines.append(f"Description: {self.package.description}")

        if self.flight:
            lines.append("")
            lines.append("=== FLIGHT DETAILS ===")
            lines.append(f"Airline: {self.flight.airline} ({self.flight.flight_number})")
            lines.append(f"Route: {self.flight.departure_airport} → {self.flight.arrival_airport}")
            lines.append(f"Departure: {self.flight.departure_datetime}")
            lines.append(f"Arrival: {self.flight.arrival_datetime}")
            if self.flight.gate:
                lines.append(f"Gate: {self.flight.gate}")
            if self.flight.seat_number:
                lines.append(f"Seat: {self.flight.seat_number}")
            flight_status = self.flight.status
            if hasattr(flight_status, "value"):
                lines.append(f"Status: {flight_status.value}")
            else:
                lines.append(f"Status: {flight_status}")

        if self.accommodation:
            lines.append("")
            lines.append("=== ACCOMMODATION DETAILS ===")
            lines.append(f"Hotel: {self.accommodation.hotel_name}")
            lines.append(f"City: {self.accommodation.city}")
            if self.accommodation.building:
                lines.append(f"Building: {self.accommodation.building}")
            if self.accommodation.floor:
                lines.append(f"Floor: {self.accommodation.floor}")
            lines.append(f"Room: {self.accommodation.room_number}")
            if self.accommodation.bed_number:
                lines.append(f"Bed: {self.accommodation.bed_number}")
            lines.append(f"Check-in: {self.accommodation.check_in}")
            lines.append(f"Check-out: {self.accommodation.check_out}")

        if self.transport:
            lines.append("")
            lines.append("=== TRANSPORT DETAILS ===")
            transport_type = self.transport.transport_type
            if hasattr(transport_type, "value"):
                transport_type_str = transport_type.value
            else:
                transport_type_str = str(transport_type)
            lines.append(f"Vehicle: {self.transport.bus_number} ({transport_type_str})")
            lines.append(f"From: {self.transport.pickup_location}")
            lines.append(f"To: {self.transport.destination}")
            lines.append(f"Pickup time: {self.transport.pickup_time}")
            lines.append(f"Driver: {self.transport.driver_name} ({self.transport.driver_phone})")

        if self.announcements:
            lines.append("")
            lines.append("=== ANNOUNCEMENTS FOR THIS PILGRIM ===")
            for a in self.announcements:
                priority = a.priority
                if hasattr(priority, "value"):
                    priority_str = priority.value.upper()
                else:
                    priority_str = str(priority).upper()
                lines.append(f"[{priority_str}] {a.title}")
                lines.append(f"  {a.message_template}")
                lines.append(f"  Valid: {a.publish_date} — {a.expiry_date}")
                lines.append("")

        result = "\n".join(lines)
        logger.info("to_prompt_context complete, length=%d", len(result))
        return result


def build_pilgrim_context(pilgrim_id: int, db: Session) -> PilgrimContext:
    """Fetch ONLY the data this pilgrim is authorized to see.

    Never fetches other pilgrims' data or untargeted records.
    """
    logger.info("Entering build_pilgrim_context for pilgrim_id=%d", pilgrim_id)

    pilgrim = db.query(User).filter(User.id == pilgrim_id, User.role == Role.pilgrim).first()
    if not pilgrim:
        raise ValueError("Pilgrim not found")

    preference = db.query(Preference).filter(Preference.pilgrim_id == pilgrim_id).first()

    package = None
    flight = None
    accommodation = None
    transport = None

    if pilgrim.package_id:
        package = db.query(Package).filter(Package.id == pilgrim.package_id).first()
        if package:
            if package.flight_id:
                flight = db.query(Flight).filter(Flight.id == package.flight_id).first()
            if package.accommodation_id:
                accommodation = db.query(Accommodation).filter(Accommodation.id == package.accommodation_id).first()
            if package.transport_id:
                transport = db.query(Transport).filter(Transport.id == package.transport_id).first()

    now = datetime.now(timezone.utc)
    conditions = [
        Announcement.target_type == TargetType.all,
        Announcement.publish_date <= now,
        Announcement.expiry_date >= now,
    ]

    from sqlalchemy import or_, and_

    target_conditions = list(conditions)

    if pilgrim.package_id:
        target_conditions.append(
            and_(Announcement.target_type == TargetType.package, Announcement.target_id == pilgrim.package_id)
        )
    target_conditions.append(
        and_(Announcement.target_type == TargetType.pilgrim, Announcement.target_id == pilgrim_id)
    )
    if package:
        if package.flight_id:
            target_conditions.append(
                and_(Announcement.target_type == TargetType.flight, Announcement.target_id == package.flight_id)
            )
        if package.accommodation_id:
            target_conditions.append(
                and_(Announcement.target_type == TargetType.accommodation, Announcement.target_id == package.accommodation_id)
            )
        if package.transport_id:
            target_conditions.append(
                and_(Announcement.target_type == TargetType.transport, Announcement.target_id == package.transport_id)
            )

    announcements = (
        db.query(Announcement)
        .filter(or_(*target_conditions))
        .order_by(Announcement.created_at.desc())
        .limit(20)
        .all()
    )

    logger.info(
        "build_pilgrim_context complete: pilgrim_id=%d, has_preference=%s, has_package=%s, has_flight=%s, has_accommodation=%s, has_transport=%s, announcements=%d",
        pilgrim_id,
        preference is not None,
        package is not None,
        flight is not None,
        accommodation is not None,
        transport is not None,
        len(announcements),
    )

    return PilgrimContext(
        pilgrim=pilgrim,
        preference=preference,
        package=package,
        flight=flight,
        accommodation=accommodation,
        transport=transport,
        announcements=announcements,
    )
