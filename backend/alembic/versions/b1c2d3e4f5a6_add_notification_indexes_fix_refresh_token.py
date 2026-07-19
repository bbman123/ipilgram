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


def _create_index_if_not_exists(index_name, table_name, columns, unique=False):
    bind = op.get_bind()
    insp = sa.inspect(bind)
    existing = [idx['name'] for idx in insp.get_indexes(table_name)]
    if index_name not in existing:
        op.create_index(index_name, table_name, columns, unique=unique)


def _drop_index_if_exists(index_name, table_name):
    bind = op.get_bind()
    insp = sa.inspect(bind)
    existing = [idx['name'] for idx in insp.get_indexes(table_name)]
    if index_name in existing:
        op.drop_index(index_name, table_name=table_name)


def upgrade() -> None:
    # Notification performance indexes
    _create_index_if_not_exists("ix_notifications_pilgrim_id", "notifications", ["pilgrim_id"])
    _create_index_if_not_exists("ix_notifications_status", "notifications", ["status"])
    _create_index_if_not_exists("ix_notifications_notification_type", "notifications", ["notification_type"])
    _create_index_if_not_exists("ix_notifications_created_at", "notifications", ["created_at"])

    # DeviceToken indexes
    _create_index_if_not_exists("ix_device_tokens_pilgrim_id", "device_tokens", ["pilgrim_id"])
    _create_index_if_not_exists("ix_device_tokens_platform", "device_tokens", ["platform"])

    # Refresh token: fix expires_at from VARCHAR to TIMESTAMP
    op.alter_column(
        "refresh_tokens",
        "expires_at",
        type_=sa.DateTime(timezone=True),
        nullable=False,
        existing_type=sa.String(),
    )


def downgrade() -> None:
    _drop_index_if_exists("ix_notifications_pilgrim_id", "notifications")
    _drop_index_if_exists("ix_notifications_status", "notifications")
    _drop_index_if_exists("ix_notifications_notification_type", "notifications")
    _drop_index_if_exists("ix_notifications_created_at", "notifications")
    _drop_index_if_exists("ix_device_tokens_pilgrim_id", "device_tokens")
    _drop_index_if_exists("ix_device_tokens_platform", "device_tokens")
    op.alter_column(
        "refresh_tokens",
        "expires_at",
        type_=sa.String(),
        nullable=False,
        existing_type=sa.DateTime(timezone=True),
    )
