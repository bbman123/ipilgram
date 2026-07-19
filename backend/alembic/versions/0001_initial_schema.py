"""initial schema — complete database for Hajj Pilgrims Management API

Revision ID: 0001
Revises:
Create Date: 2026-07-20 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()

    result = bind.execute(
        sa.text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'flights')")
    )
    if result.scalar():
        return

    ROLE_ENUM = sa.Enum("admin", "pilgrim", name="role", create_type=False)
    FLIGHT_STATUS_ENUM = sa.Enum(
        "scheduled", "confirmed", "boarding", "departed",
        "in_air", "landed", "cancelled", "delayed",
        name="flightstatus", create_type=False,
    )
    TRANSPORT_TYPE_ENUM = sa.Enum("bus", "van", "taxi", "car", "other", name="transporttype", create_type=False)
    TARGET_TYPE_ENUM = sa.Enum(
        "all", "pilgrim", "package", "flight", "accommodation", "transport",
        name="targettype", create_type=False,
    )
    ANNOUNCEMENT_PRIORITY_ENUM = sa.Enum("low", "medium", "high", "urgent", name="announcementpriority", create_type=False)
    NOTIFICATION_TYPE_ENUM = sa.Enum(
        "flight_reminder", "accommodation_checkin", "accommodation_checkout",
        "transport_reminder", "return_flight", "emergency", "broadcast", "announcement",
        name="notificationtype", create_type=False,
    )
    NOTIFICATION_STATUS_ENUM = sa.Enum("pending", "scheduled", "sent", "failed", "read", name="notificationstatus", create_type=False)
    PREFERRED_LANGUAGE_ENUM = sa.Enum("English", "Hausa", "Yoruba", "Igbo", "Arabic", name="preferredlanguage", create_type=False)
    DELIVERY_MODE_ENUM = sa.Enum("Text", "Audio", "Text + Audio", name="deliverymode", create_type=False)

    # =========================================================================
    # flights — no foreign keys, created first
    # =========================================================================
    op.create_table(
        "flights",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("airline", sa.String(255), nullable=False),
        sa.Column("flight_number", sa.String(50), nullable=False),
        sa.Column("departure_airport", sa.String(100), nullable=False),
        sa.Column("arrival_airport", sa.String(100), nullable=False),
        sa.Column("departure_datetime", sa.DateTime(), nullable=False),
        sa.Column("arrival_datetime", sa.DateTime(), nullable=False),
        sa.Column("gate", sa.String(20), nullable=True),
        sa.Column("seat_number", sa.String(20), nullable=True),
        sa.Column("status", FLIGHT_STATUS_ENUM, nullable=False, server_default="scheduled"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # =========================================================================
    # accommodations — no foreign keys
    # =========================================================================
    op.create_table(
        "accommodations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("hotel_name", sa.String(255), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("building", sa.String(100), nullable=True),
        sa.Column("floor", sa.String(20), nullable=True),
        sa.Column("room_number", sa.String(20), nullable=False),
        sa.Column("bed_number", sa.String(20), nullable=True),
        sa.Column("address", sa.String(500), nullable=True),
        sa.Column("check_in", sa.DateTime(), nullable=False),
        sa.Column("check_out", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # =========================================================================
    # transports — no foreign keys
    # =========================================================================
    op.create_table(
        "transports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("bus_number", sa.String(50), nullable=False),
        sa.Column("pickup_location", sa.String(255), nullable=False),
        sa.Column("destination", sa.String(255), nullable=False),
        sa.Column("pickup_time", sa.DateTime(), nullable=False),
        sa.Column("driver_name", sa.String(255), nullable=False),
        sa.Column("driver_phone", sa.String(50), nullable=False),
        sa.Column("transport_type", TRANSPORT_TYPE_ENUM, nullable=False, server_default="bus"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # =========================================================================
    # packages — FKs to flights, accommodations, transports
    # =========================================================================
    op.create_table(
        "packages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("flight_id", sa.Integer(), nullable=True),
        sa.Column("accommodation_id", sa.Integer(), nullable=True),
        sa.Column("transport_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["flight_id"], ["flights.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["accommodation_id"], ["accommodations.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["transport_id"], ["transports.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_packages_flight_id", "packages", ["flight_id"])
    op.create_index("ix_packages_accommodation_id", "packages", ["accommodation_id"])
    op.create_index("ix_packages_transport_id", "packages", ["transport_id"])

    # =========================================================================
    # users — FK to packages (must come after packages)
    # =========================================================================
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", ROLE_ENUM, nullable=False, server_default="pilgrim"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("package_id", sa.Integer(), nullable=True),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("nationality", sa.String(100), nullable=True),
        sa.Column("passport_number", sa.String(50), nullable=True),
        sa.Column("emergency_contact", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["package_id"], ["packages.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_package_id", "users", ["package_id"])

    # =========================================================================
    # refresh_tokens — FK to users
    # =========================================================================
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("token", sa.String(500), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_refresh_tokens_token", "refresh_tokens", ["token"], unique=True)
    op.create_index("ix_refresh_tokens_user_id", "refresh_tokens", ["user_id"])
    op.create_index("ix_refresh_tokens_expires_at", "refresh_tokens", ["expires_at"])

    # =========================================================================
    # notifications — FK to users
    # =========================================================================
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("pilgrim_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("notification_type", NOTIFICATION_TYPE_ENUM, nullable=False),
        sa.Column("status", NOTIFICATION_STATUS_ENUM, nullable=False, server_default="pending"),
        sa.Column("scheduled_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delivery_mode", sa.String(20), nullable=True, server_default="text"),
        sa.Column("language", sa.String(20), nullable=True, server_default="English"),
        sa.Column("audio_url", sa.String(500), nullable=True),
        sa.Column("source_type", sa.String(50), nullable=True),
        sa.Column("source_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["pilgrim_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_notifications_pilgrim_id", "notifications", ["pilgrim_id"])
    op.create_index("ix_notifications_scheduled_time", "notifications", ["scheduled_time"])
    op.create_index("ix_notifications_source_type", "notifications", ["source_type"])

    # =========================================================================
    # device_tokens — FK to users
    # =========================================================================
    op.create_table(
        "device_tokens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("pilgrim_id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(512), nullable=False),
        sa.Column("platform", sa.String(20), nullable=False, server_default="android"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["pilgrim_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_device_tokens_pilgrim_id", "device_tokens", ["pilgrim_id"])
    op.create_unique_constraint("uq_device_tokens_token", "device_tokens", ["token"])

    # =========================================================================
    # preferences — FK to users (unique)
    # =========================================================================
    op.create_table(
        "preferences",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("pilgrim_id", sa.Integer(), nullable=False),
        sa.Column("preferred_language", PREFERRED_LANGUAGE_ENUM, nullable=False, server_default="English"),
        sa.Column("delivery_mode", DELIVERY_MODE_ENUM, nullable=False, server_default="Text"),
        sa.Column("font_size", sa.Integer(), nullable=False, server_default=sa.text("16")),
        sa.Column("notifications_enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["pilgrim_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("pilgrim_id"),
    )

    # =========================================================================
    # announcements — no foreign keys (target_id is polymorphic)
    # =========================================================================
    op.create_table(
        "announcements",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("message_template", sa.Text(), nullable=False),
        sa.Column("priority", ANNOUNCEMENT_PRIORITY_ENUM, nullable=False, server_default="medium"),
        sa.Column("target_type", TARGET_TYPE_ENUM, nullable=False, server_default="all"),
        sa.Column("target_id", sa.Integer(), nullable=True),
        sa.Column("publish_date", sa.DateTime(), nullable=False),
        sa.Column("expiry_date", sa.DateTime(), nullable=False),
        sa.Column("include_package_details", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("include_flight_details", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("include_transport_details", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("include_accommodation_details", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("send_as_notification", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_announcements_target", "announcements", ["target_type", "target_id"])


def downgrade() -> None:
    op.drop_table("announcements")
    op.drop_table("preferences")
    op.drop_table("device_tokens")
    op.drop_table("notifications")
    op.drop_table("refresh_tokens")
    op.drop_table("users")
    op.drop_table("packages")
    op.drop_table("transports")
    op.drop_table("accommodations")
    op.drop_table("flights")

    for name in [
        "deliverymode", "preferredlanguage", "notificationstatus",
        "notificationtype", "announcementpriority", "targettype",
        "transporttype", "flightstatus", "role",
    ]:
        op.execute(sa.text(f"DROP TYPE IF EXISTS {name}"))
