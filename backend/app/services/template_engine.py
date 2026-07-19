"""Replaces template placeholders with pilgrim-specific data.

Used by the announcements API when pilgrims retrieve their personalized announcements.
"""

import re
import logging

from sqlalchemy.orm import Session

from app.models.user import User, Role
from app.models.package import Package
from app.models.flight import Flight
from app.models.accommodation import Accommodation
from app.models.transport import Transport

logger = logging.getLogger(__name__)


def _format_time(dt) -> str:
    if dt is None:
        return "TBA"
    if hasattr(dt, "strftime"):
        return dt.strftime("%I:%M %p")
    return str(dt)


def _format_date(dt) -> str:
    if dt is None:
        return "TBA"
    if hasattr(dt, "strftime"):
        return dt.strftime("%d %b %Y")
    return str(dt)


def build_replacement_map(pilgrim_id: int, db: Session) -> dict[str, str]:
    """Build a dict of placeholder -> value for the given pilgrim."""
    pilgrim = db.query(User).filter(User.id == pilgrim_id, User.role == Role.pilgrim).first()
    if not pilgrim:
        return {}

    replacements = {
        "pilgrim_name": pilgrim.full_name or "Pilgrim",
    }

    if pilgrim.package_id:
        package = db.query(Package).filter(Package.id == pilgrim.package_id).first()
        if package:
            replacements["package_name"] = package.name

            if package.flight_id:
                flight = db.query(Flight).filter(Flight.id == package.flight_id).first()
                if flight:
                    replacements.update({
                        "flight_number": flight.flight_number,
                        "airline": flight.airline,
                        "departure_airport": flight.departure_airport,
                        "arrival_airport": flight.arrival_airport,
                        "departure_time": _format_time(flight.departure_datetime),
                        "arrival_time": _format_time(flight.arrival_datetime),
                        "gate": flight.gate or "TBA",
                        "seat": flight.seat_number or "TBA",
                    })

            if package.accommodation_id:
                acc = db.query(Accommodation).filter(Accommodation.id == package.accommodation_id).first()
                if acc:
                    replacements.update({
                        "hotel_name": acc.hotel_name,
                        "city": acc.city,
                        "room_number": acc.room_number,
                        "check_in_time": _format_time(acc.check_in),
                        "check_out_time": _format_time(acc.check_out),
                    })

            if package.transport_id:
                transport = db.query(Transport).filter(Transport.id == package.transport_id).first()
                if transport:
                    replacements.update({
                        "pickup_location": transport.pickup_location,
                        "destination": transport.destination,
                        "pickup_time": _format_time(transport.pickup_time),
                        "driver_name": transport.driver_name,
                        "driver_phone": transport.driver_phone,
                    })

    return replacements


def replace_placeholders(template: str, replacements: dict[str, str]) -> str:
    """Replace {{placeholder}} patterns in the template string."""
    result = template
    for key, value in replacements.items():
        pattern = "{{" + key + "}}"
        result = result.replace(pattern, value)

    remaining = re.findall(r"\{\{(\w+)\}\}", result)
    if remaining:
        logger.warning("Unresolved placeholders in template: %s", remaining)

    return result
