"""Notification Engine — Auto-generates personalized notifications for pilgrims.

Based on each pilgrim's assigned package (flight, accommodation, transport),
the engine creates time-based notifications and schedules them for delivery.

Runs as a background task on a configurable interval.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Sequence

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user import User, Role
from app.models.package import Package
from app.models.flight import Flight
from app.models.accommodation import Accommodation
from app.models.transport import Transport
from app.models.notification import (
    Notification,
    NotificationType,
    NotificationStatus,
)

logger = logging.getLogger("hajj_notification_engine")

RULES = [
    {
        "type": NotificationType.flight_reminder,
        "title_template": "Flight in {delta}",
        "message_template": "Your flight {flight_number} ({airline}) departs from {departure_airport} at {departure_time}. Please prepare for departure.",
        "time_before": timedelta(days=2),
        "source_type": "flight",
    },
    {
        "type": NotificationType.flight_reminder,
        "title_template": "Flight tomorrow",
        "message_template": "Your flight {flight_number} ({airline}) departs from {departure_airport} at {departure_time}. Make sure your documents are ready.",
        "time_before": timedelta(days=1),
        "source_type": "flight",
    },
    {
        "type": NotificationType.flight_reminder,
        "title_template": "Travel day reminder",
        "message_template": "Today is your travel day! Your flight {flight_number} departs from {departure_airport} at {departure_time}.",
        "time_before": timedelta(hours=0),
        "source_type": "flight",
    },
    {
        "type": NotificationType.flight_reminder,
        "title_template": "Flight in 12 hours",
        "message_template": "Your flight {flight_number} departs in 12 hours from {departure_airport} at {departure_time}. Please be at the airport on time.",
        "time_before": timedelta(hours=12),
        "source_type": "flight",
    },
    {
        "type": NotificationType.flight_reminder,
        "title_template": "Flight in 4 hours",
        "message_template": "Your flight {flight_number} departs in 4 hours from {departure_airport} at {departure_time}. Head to gate {gate} now.",
        "time_before": timedelta(hours=4),
        "source_type": "flight",
    },
    {
        "type": NotificationType.accommodation_checkin,
        "title_template": "Hotel check-in reminder",
        "message_template": "Check-in at {hotel_name} is available from {check_in_time}. Your room is {room_number} in {city}.",
        "time_before": timedelta(hours=6),
        "source_type": "accommodation",
    },
    {
        "type": NotificationType.accommodation_checkout,
        "title_template": "Hotel check-out reminder",
        "message_template": "Check-out from {hotel_name} is at {check_out_time}. Please settle any outstanding charges and return your room key.",
        "time_before": timedelta(hours=6),
        "source_type": "accommodation",
    },
    {
        "type": NotificationType.transport_reminder,
        "title_template": "Transport pickup reminder",
        "message_template": "Your {transport_type} pickup is at {pickup_location} at {pickup_time}. Driver: {driver_name} ({driver_phone}).",
        "time_before": timedelta(hours=2),
        "source_type": "transport",
    },
    {
        "type": NotificationType.return_flight,
        "title_template": "Return flight reminder",
        "message_template": "Your return flight {flight_number} departs from {arrival_airport} at {arrival_time}. Please arrive at the airport early.",
        "time_before": timedelta(days=1),
        "source_type": "flight",
    },
]


def _format_time_delta(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    if total_seconds <= 0:
        return "today"
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    if days > 0 and hours > 0:
        return f"{days} day{'s' if days != 1 else ''} and {hours} hour{'s' if hours != 1 else ''}"
    if days > 0:
        return f"{days} day{'s' if days != 1 else ''}"
    if hours > 0:
        return f"{hours} hour{'s' if hours != 1 else ''}"
    return "less than an hour"


def _build_flight_context(flight: Flight) -> dict:
    dep = flight.departure_datetime
    arr = flight.arrival_datetime
    return {
        "flight_number": flight.flight_number,
        "airline": flight.airline,
        "departure_airport": flight.departure_airport,
        "arrival_airport": flight.arrival_airport,
        "departure_time": dep.strftime("%I:%M %p") if dep else "TBA",
        "arrival_time": arr.strftime("%I:%M %p") if arr else "TBA",
        "gate": flight.gate or "TBA",
        "seat": flight.seat_number or "TBA",
        "status": flight.status.value,
    }


def _build_accommodation_context(acc: Accommodation) -> dict:
    return {
        "hotel_name": acc.hotel_name,
        "city": acc.city,
        "room_number": acc.room_number,
        "check_in_time": acc.check_in.strftime("%I:%M %p") if acc.check_in else "TBA",
        "check_out_time": acc.check_out.strftime("%I:%M %p") if acc.check_out else "TBA",
    }


def _build_transport_context(transport: Transport) -> dict:
    return {
        "transport_type": transport.transport_type.value,
        "pickup_location": transport.pickup_location,
        "destination": transport.destination,
        "pickup_time": transport.pickup_time.strftime("%I:%M %p") if transport.pickup_time else "TBA",
        "driver_name": transport.driver_name,
        "driver_phone": transport.driver_phone,
    }


def _generate_notifications_for_pilgrim(
    pilgrim: User,
    package: Package,
    flight: Flight | None,
    accommodation: Accommodation | None,
    transport: Transport | None,
    db: Session,
) -> list[Notification]:
    """Generate all applicable notifications for a single pilgrim based on their package."""
    now = datetime.now(timezone.utc)
    created = []

    for rule in RULES:
        source_id = None
        context = {}

        if rule["source_type"] == "flight" and flight:
            source_id = flight.id
            context = _build_flight_context(flight)

            dep_dt = flight.departure_datetime
            if dep_dt.tzinfo is None:
                dep_dt = dep_dt.replace(tzinfo=timezone.utc)

            scheduled_time = dep_dt - rule["time_before"]
            if rule["type"] == NotificationType.return_flight:
                scheduled_time = dep_dt - rule["time_before"]

            if scheduled_time < now:
                continue

        elif rule["source_type"] == "accommodation" and accommodation:
            source_id = accommodation.id
            context = _build_accommodation_context(accommodation)

            if rule["type"] == NotificationType.accommodation_checkin:
                check_in = accommodation.check_in
                if check_in.tzinfo is None:
                    check_in = check_in.replace(tzinfo=timezone.utc)
                scheduled_time = check_in - rule["time_before"]
            else:
                check_out = accommodation.check_out
                if check_out.tzinfo is None:
                    check_out = check_out.replace(tzinfo=timezone.utc)
                scheduled_time = check_out - rule["time_before"]

            if scheduled_time < now:
                continue

        elif rule["source_type"] == "transport" and transport:
            source_id = transport.id
            context = _build_transport_context(transport)

            pickup = transport.pickup_time
            if pickup.tzinfo is None:
                pickup = pickup.replace(tzinfo=timezone.utc)
            scheduled_time = pickup - rule["time_before"]

            if scheduled_time < now:
                continue
        else:
            continue

        time_delta = rule["time_before"]
        if scheduled_time > now:
            time_delta = scheduled_time - now
        context["delta"] = _format_time_delta(time_delta)

        title = rule["title_template"].format(**context)
        message = rule["message_template"].format(**context)

        existing = (
            db.query(Notification)
            .filter(
                Notification.pilgrim_id == pilgrim.id,
                Notification.notification_type == rule["type"],
                Notification.source_type == rule["source_type"],
                Notification.source_id == source_id,
            )
            .first()
        )
        if existing:
            continue

        notification = Notification(
            pilgrim_id=pilgrim.id,
            title=title,
            message=message,
            notification_type=rule["type"],
            status=NotificationStatus.scheduled,
            scheduled_time=scheduled_time,
            source_type=rule["source_type"],
            source_id=source_id,
        )
        db.add(notification)
        created.append(notification)

    return created


def run_notification_engine():
    """Main engine loop — scan all pilgrims and generate/update notifications.

    Designed to be called periodically by the scheduler.
    """
    logger.info("Notification engine run started")
    db = SessionLocal()
    try:
        pilgrims = (
            db.query(User)
            .filter(User.role == Role.pilgrim, User.is_active == True)
            .all()
        )

        total_created = 0
        for pilgrim in pilgrims:
            if not pilgrim.package_id:
                continue

            package = db.query(Package).filter(Package.id == pilgrim.package_id).first()
            if not package:
                continue

            flight = db.query(Flight).filter(Flight.id == package.flight_id).first() if package.flight_id else None
            accommodation = db.query(Accommodation).filter(Accommodation.id == package.accommodation_id).first() if package.accommodation_id else None
            transport = db.query(Transport).filter(Transport.id == package.transport_id).first() if package.transport_id else None

            created = _generate_notifications_for_pilgrim(pilgrim, package, flight, accommodation, transport, db)
            total_created += len(created)

        now = datetime.now(timezone.utc)
        pending = (
            db.query(Notification)
            .filter(
                Notification.status == NotificationStatus.scheduled,
                Notification.scheduled_time <= now,
            )
            .all()
        )

        for n in pending:
            n.status = NotificationStatus.pending
            n.sent_at = now

        if total_created > 0 or pending:
            db.commit()
            logger.info(
                "Notification engine completed: %d created, %d marked pending",
                total_created,
                len(pending),
            )
        else:
            logger.info("Notification engine completed: no new notifications")

    except Exception as exc:
        db.rollback()
        logger.error("Notification engine error: %s", exc, exc_info=True)
    finally:
        db.close()
