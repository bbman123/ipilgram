"""Add notification indexes, fix refresh_token expires_at type

Revision ID: b1c2d3e4f5a6
Revises: f1a2b3c4d5e6
Create Date: 2026-07-19
"""
from alembic import op
import sqlalchemy as sa


revision = "b1c2d3e4f5a6"
down_revision = "f1a2b3c4d5e6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Notification performance indexes
    op.create_index("ix_notifications_pilgrim_id", "notifications", ["pilgrim_id"])
    op.create_index("ix_notifications_status", "notifications", ["status"])
    op.create_index("ix_notifications_notification_type", "notifications", ["notification_type"])
    op.create_index("ix_notifications_created_at", "notifications", ["created_at"])

    # DeviceToken indexes
    op.create_index("ix_device_tokens_pilgrim_id", "device_tokens", ["pilgrim_id"])
    op.create_index("ix_device_tokens_platform", "device_tokens", ["platform"])

    # Refresh token: fix expires_at from VARCHAR to TIMESTAMP
    op.alter_column(
        "refresh_tokens",
        "expires_at",
        type_=sa.DateTime(timezone=True),
        nullable=False,
        existing_type=sa.String(),
    )


def downgrade() -> None:
    op.drop_index("ix_notifications_pilgrim_id", table_name="notifications")
    op.drop_index("ix_notifications_status", table_name="notifications")
    op.drop_index("ix_notifications_notification_type", table_name="notifications")
    op.drop_index("ix_notifications_created_at", table_name="notifications")
    op.drop_index("ix_device_tokens_pilgrim_id", table_name="device_tokens")
    op.drop_index("ix_device_tokens_platform", table_name="device_tokens")
    op.alter_column(
        "refresh_tokens",
        "expires_at",
        type_=sa.String(),
        nullable=False,
        existing_type=sa.DateTime(timezone=True),
    )
