import sys
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def seed():
    try:
        from app.core.database import SessionLocal
        from app.core.security import hash_password
        from app.models.user import User, Role
        from app.models.flight import Flight, FlightStatus
        from app.models.accommodation import Accommodation
        from app.models.transport import Transport, TransportType
        from app.models.package import Package
        from app.models.announcement import Announcement, TargetType, AnnouncementPriority
        from app.models.preference import Preference, PreferredLanguage, DeliveryMode
        from app.models.notification import Notification, NotificationType, NotificationStatus

        db = SessionLocal()
        try:
            if db.query(Flight).count() > 0:
                print("SEED: Flight data already exists, skipping.")
                return

            now = datetime.now(timezone.utc)
            hajj_date = now + timedelta(days=30)

            print("SEED: Creating flights...")
            flights = [
                Flight(
                    airline="Air Peace",
                    flight_number="AP-7850",
                    departure_airport="Murtala Muhammed International Airport (LOS)",
                    arrival_airport="King Abdulaziz International Airport (JED)",
                    departure_datetime=hajj_date - timedelta(days=2),
                    arrival_datetime=hajj_date - timedelta(days=2) + timedelta(hours=7),
                    gate="A12",
                    seat_number="14C",
                    status=FlightStatus.confirmed,
                ),
                Flight(
                    airline="Ethiopian Airlines",
                    flight_number="ET-900",
                    departure_airport="Murtala Muhammed International Airport (LOS)",
                    arrival_airport="King Abdulaziz International Airport (JED)",
                    departure_datetime=hajj_date - timedelta(days=1),
                    arrival_datetime=hajj_date - timedelta(days=1) + timedelta(hours=8),
                    gate="B7",
                    seat_number="22A",
                    status=FlightStatus.scheduled,
                ),
                Flight(
                    airline="Saudia",
                    flight_number="SV-401",
                    departure_airport="Nnamdi Azikiwe International Airport (ABV)",
                    arrival_airport="Prince Mohammad Bin Abdulaziz Airport (MED)",
                    departure_datetime=hajj_date - timedelta(days=3),
                    arrival_datetime=hajj_date - timedelta(days=3) + timedelta(hours=6, minutes=30),
                    gate="C3",
                    seat_number="8F",
                    status=FlightStatus.confirmed,
                ),
                Flight(
                    airline="Max Air",
                    flight_number="NM-710",
                    departure_airport="Mallam Aminu Kano International Airport (KAN)",
                    arrival_airport="King Abdulaziz International Airport (JED)",
                    departure_datetime=hajj_date,
                    arrival_datetime=hajj_date + timedelta(hours=7, minutes=15),
                    gate="D5",
                    seat_number="31B",
                    status=FlightStatus.scheduled,
                ),
            ]
            db.add_all(flights)
            db.flush()

            print("SEED: Creating accommodations...")
            accommodations = [
                Accommodation(
                    hotel_name="Al Marwa Rayyhan by Rotana",
                    city="Makkah",
                    building="Tower A",
                    floor="7th",
                    room_number="712",
                    bed_number="1",
                    address="Ajyad Street, Abraj Al Bait, Makkah",
                    check_in=hajj_date - timedelta(days=1),
                    check_out=hajj_date + timedelta(days=10),
                ),
                Accommodation(
                    hotel_name="Pullman Zamzam Makkah",
                    city="Makkah",
                    building="Main Tower",
                    floor="12th",
                    room_number="1205",
                    bed_number="2",
                    address="Opposite King Fahd Gate, Masjid al-Haram",
                    check_in=hajj_date - timedelta(days=1),
                    check_out=hajj_date + timedelta(days=10),
                ),
                Accommodation(
                    hotel_name="Madinah Hilton",
                    city="Madinah",
                    building="West Wing",
                    floor="5th",
                    room_number="503",
                    bed_number="1",
                    address="King Abdul Aziz Road, Madinah",
                    check_in=hajj_date + timedelta(days=10),
                    check_out=hajj_date + timedelta(days=14),
                ),
                Accommodation(
                    hotel_name="Al Aqeeq Madinah Hotel",
                    city="Makkah",
                    building="Block B",
                    floor="3rd",
                    room_number="308",
                    bed_number="2",
                    address="Al Aqeeq District, Makkah",
                    check_in=hajj_date - timedelta(days=2),
                    check_out=hajj_date + timedelta(days=12),
                ),
            ]
            db.add_all(accommodations)
            db.flush()

            print("SEED: Creating transports...")
            transports = [
                Transport(
                    bus_number="HJ-001",
                    pickup_location="Jeddah Airport Terminal 1",
                    destination="Makkah Grand Mosque",
                    pickup_time=hajj_date - timedelta(days=2) + timedelta(hours=8),
                    driver_name="Ibrahim Musa",
                    driver_phone="+966501234567",
                    transport_type=TransportType.bus,
                ),
                Transport(
                    bus_number="HJ-002",
                    pickup_location="Makkah Hotel Lobby",
                    destination="Mina Camp",
                    pickup_time=hajj_date + timedelta(days=7),
                    driver_name="Abdullah Suleiman",
                    driver_phone="+966509876543",
                    transport_type=TransportType.bus,
                ),
                Transport(
                    bus_number="HJ-003",
                    pickup_location="Mina Camp",
                    destination="Arafat Plain",
                    pickup_time=hajj_date + timedelta(days=8),
                    driver_name="Yusuf Abdullahi",
                    driver_phone="+966504567890",
                    transport_type=TransportType.bus,
                ),
                Transport(
                    bus_number="VN-101",
                    pickup_location="Madinah Airport",
                    destination="Madinah Hotel",
                    pickup_time=hajj_date + timedelta(days=10) + timedelta(hours=2),
                    driver_name="Omar Farouk",
                    driver_phone="+966503216549",
                    transport_type=TransportType.van,
                ),
            ]
            db.add_all(transports)
            db.flush()

            print("SEED: Creating packages...")
            packages = [
                Package(
                    name="Hajj Package - Premium",
                    description="All-inclusive premium Hajj package with 5-star hotel, direct flights, and luxury bus transport.",
                    flight_id=flights[0].id,
                    accommodation_id=accommodations[0].id,
                    transport_id=transports[0].id,
                ),
                Package(
                    name="Hajj Package - Standard",
                    description="Standard Hajj package with 4-star hotel, economy flights, and shared bus transport.",
                    flight_id=flights[1].id,
                    accommodation_id=accommodations[1].id,
                    transport_id=transports[1].id,
                ),
                Package(
                    name="Hajj Package - Economy",
                    description="Budget-friendly Hajj package with 3-star accommodation and basic transport.",
                    flight_id=flights[3].id,
                    accommodation_id=accommodations[3].id,
                    transport_id=transports[3].id,
                ),
            ]
            db.add_all(packages)
            db.flush()

            print("SEED: Creating pilgrims...")
            pilgrims = [
                User(
                    email="abdullah.ibrahim@example.com",
                    full_name="Abdullah Ibrahim",
                    hashed_password=hash_password("pilgrim123"),
                    role=Role.pilgrim,
                    package_id=packages[0].id,
                    phone="+2348012345678",
                    nationality="Nigerian",
                    passport_number="A12345678",
                    emergency_contact="Fatima Ibrahim - +2348098765432",
                ),
                User(
                    email="fatima.mohammed@example.com",
                    full_name="Fatima Mohammed",
                    hashed_password=hash_password("pilgrim123"),
                    role=Role.pilgrim,
                    package_id=packages[0].id,
                    phone="+2348023456789",
                    nationality="Nigerian",
                    passport_number="B23456789",
                    emergency_contact="Mohammed Ali - +2348087654321",
                ),
                User(
                    email="usman.bello@example.com",
                    full_name="Usman Bello",
                    hashed_password=hash_password("pilgrim123"),
                    role=Role.pilgrim,
                    package_id=packages[1].id,
                    phone="+2348034567890",
                    nationality="Nigerian",
                    passport_number="C34567890",
                    emergency_contact="Aisha Bello - +2348076543210",
                ),
                User(
                    email="amina.yusuf@example.com",
                    full_name="Amina Yusuf",
                    hashed_password=hash_password("pilgrim123"),
                    role=Role.pilgrim,
                    package_id=packages[1].id,
                    phone="+2348045678901",
                    nationality="Nigerian",
                    passport_number="D45678901",
                    emergency_contact="Ibrahim Yusuf - +2348065432109",
                ),
                User(
                    email="hassan.ali@example.com",
                    full_name="Hassan Ali",
                    hashed_password=hash_password("pilgrim123"),
                    role=Role.pilgrim,
                    package_id=packages[2].id,
                    phone="+2348056789012",
                    nationality="Nigerian",
                    passport_number="E56789012",
                    emergency_contact="Zainab Ali - +2348054321098",
                ),
                User(
                    email="zainab.abubakar@example.com",
                    full_name="Zainab Abubakar",
                    hashed_password=hash_password("pilgrim123"),
                    role=Role.pilgrim,
                    package_id=packages[2].id,
                    phone="+2348067890123",
                    nationality="Nigerian",
                    passport_number="F67890123",
                    emergency_contact="Abubakar Garba - +2348043210987",
                ),
            ]
            db.add_all(pilgrims)
            db.flush()

            print("SEED: Creating preferences...")
            prefs = [
                Preference(pilgrim_id=pilgrims[0].id, preferred_language=PreferredLanguage.English, delivery_mode=DeliveryMode.Text, font_size=18, notifications_enabled=True),
                Preference(pilgrim_id=pilgrims[1].id, preferred_language=PreferredLanguage.Hausa, delivery_mode=DeliveryMode.Audio, font_size=16, notifications_enabled=True),
                Preference(pilgrim_id=pilgrims[2].id, preferred_language=PreferredLanguage.English, delivery_mode=DeliveryMode.TextPlusAudio, font_size=20, notifications_enabled=True),
                Preference(pilgrim_id=pilgrims[3].id, preferred_language=PreferredLanguage.Yoruba, delivery_mode=DeliveryMode.Text, font_size=14, notifications_enabled=True),
                Preference(pilgrim_id=pilgrims[4].id, preferred_language=PreferredLanguage.Hausa, delivery_mode=DeliveryMode.Audio, font_size=22, notifications_enabled=True),
                Preference(pilgrim_id=pilgrims[5].id, preferred_language=PreferredLanguage.Igbo, delivery_mode=DeliveryMode.TextPlusAudio, font_size=16, notifications_enabled=False),
            ]
            db.add_all(prefs)

            print("SEED: Creating announcements...")
            announcements = [
                Announcement(
                    title="Welcome to Hajj 2026",
                    message_template="Dear {{pilgrim_name}}, welcome to Hajj 2026! Your package {{package_name}} includes flight {{flight_number}} with {{airline}}. Please arrive at {{departure_airport}} at least 3 hours before departure.",
                    priority=AnnouncementPriority.high,
                    target_type=TargetType.all,
                    publish_date=now - timedelta(days=7),
                    expiry_date=hajj_date + timedelta(days=15),
                    include_package_details=True,
                    include_flight_details=True,
                    send_as_notification=True,
                ),
                Announcement(
                    title="Flight Departure Reminder",
                    message_template="Dear {{pilgrim_name}}, your flight {{flight_number}} departs from {{departure_airport}} on {{departure_time}}. Gate: {{gate}}, Seat: {{seat}}. Please be at the airport early.",
                    priority=AnnouncementPriority.urgent,
                    target_type=TargetType.all,
                    publish_date=hajj_date - timedelta(days=3),
                    expiry_date=hajj_date,
                    include_flight_details=True,
                    send_as_notification=True,
                ),
                Announcement(
                    title="Hotel Check-In Instructions",
                    message_template="Dear {{pilgrim_name}}, you will be staying at {{hotel_name}} in {{city}}, Room {{room_number}}. Check-in: {{check_in_time}}, Check-out: {{check_out_time}}. Please keep your ID handy.",
                    priority=AnnouncementPriority.medium,
                    target_type=TargetType.all,
                    publish_date=hajj_date - timedelta(days=2),
                    expiry_date=hajj_date + timedelta(days=12),
                    include_accommodation_details=True,
                    send_as_notification=True,
                ),
                Announcement(
                    title="Transport to Mina",
                    message_template="Dear {{pilgrim_name}}, buses to Mina will depart from {{pickup_location}} at {{pickup_time}}. Driver: {{driver_name}} ({{driver_phone}}). Bus number: {{destination}}. Please be ready 30 minutes early.",
                    priority=AnnouncementPriority.high,
                    target_type=TargetType.all,
                    publish_date=hajj_date + timedelta(days=5),
                    expiry_date=hajj_date + timedelta(days=9),
                    include_transport_details=True,
                    send_as_notification=True,
                ),
            ]
            db.add_all(announcements)

            print("SEED: Creating sample notifications...")
            notifications = [
                Notification(
                    pilgrim_id=pilgrims[0].id,
                    title="Welcome to Hajj 2026",
                    message="Dear Abdullah Ibrahim, welcome to Hajj 2026! Your Hajj Package - Premium includes flight AP-7850 with Air Peace. Please arrive at Murtala Muhammed International Airport (LOS) at least 3 hours before departure.",
                    notification_type=NotificationType.announcement,
                    status=NotificationStatus.sent,
                    sent_at=now - timedelta(days=6),
                    delivery_mode="text",
                    language="English",
                    source_type="announcement",
                ),
                Notification(
                    pilgrim_id=pilgrims[1].id,
                    title="Welcome to Hajj 2026",
                    message="Dear Fatima Mohammed, barka da zuwa Hajj 2026! Hakkin ku na Hajj Package - Premium ya ƙunshi jirgin AP-7850 tare da Air Peace. Da fatan za a iso a Murtala Muhammed International Airport (LOS) aƙalla awanni 3 kafin fara jirgin.",
                    notification_type=NotificationType.announcement,
                    status=NotificationStatus.sent,
                    sent_at=now - timedelta(days=6),
                    delivery_mode="audio",
                    language="Hausa",
                    source_type="announcement",
                ),
                Notification(
                    pilgrim_id=pilgrims[0].id,
                    title="Flight Departure Reminder",
                    message="Dear Abdullah Ibrahim, your flight AP-7850 departs from Murtala Muhammed International Airport (LOS) on June 3, 2026. Gate: A12, Seat: 14C. Please be at the airport early.",
                    notification_type=NotificationType.flight_reminder,
                    status=NotificationStatus.pending,
                    delivery_mode="text",
                    language="English",
                    source_type="announcement",
                ),
                Notification(
                    pilgrim_id=pilgrims[4].id,
                    title="Hotel Check-In",
                    message="Dear Hassan Ali, you will be staying at Al Aqeeq Madinah Hotel in Makkah, Room 308. Check-in: June 3, 2026. Please keep your ID handy.",
                    notification_type=NotificationType.accommodation_checkin,
                    status=NotificationStatus.pending,
                    delivery_mode="audio",
                    language="Hausa",
                    source_type="announcement",
                ),
            ]
            db.add_all(notifications)

            db.commit()
            print("SEED: All data created successfully!")
            print(f"  - 4 flights")
            print(f"  - 4 accommodations")
            print(f"  - 4 transports")
            print(f"  - 3 packages")
            print(f"  - 6 pilgrims (password: pilgrim123)")
            print(f"  - 6 preferences")
            print(f"  - 4 announcements")
            print(f"  - 4 notifications")
        finally:
            db.close()

    except Exception as e:
        print(f"SEED ERROR: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    seed()
