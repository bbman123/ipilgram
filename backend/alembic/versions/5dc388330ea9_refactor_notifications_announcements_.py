"""refactor notifications, announcements, and add package enhancements

Revision ID: 5dc388330ea9
Revises: df351592da15
Create Date: 2026-07-19 16:49:03.165357
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5dc388330ea9'
down_revision: Union[str, None] = 'df351592da15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # === ANNOUNCEMENTS: rename message -> message_template, add new columns ===
    op.alter_column('announcements', 'message', new_column_name='message_template')
    op.add_column('announcements', sa.Column('include_package_details', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('announcements', sa.Column('include_flight_details', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('announcements', sa.Column('include_transport_details', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('announcements', sa.Column('include_accommodation_details', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('announcements', sa.Column('send_as_notification', sa.Boolean(), server_default='false', nullable=False))

    # === NOTIFICATIONS: redesign columns ===
    op.add_column('notifications', sa.Column('message', sa.Text(), nullable=True))
    op.add_column('notifications', sa.Column('scheduled_time', sa.DateTime(timezone=True), nullable=True))
    op.add_column('notifications', sa.Column('read_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('notifications', sa.Column('delivery_mode', sa.String(20), nullable=True))
    op.add_column('notifications', sa.Column('language', sa.String(20), nullable=True))
    op.add_column('notifications', sa.Column('audio_url', sa.String(500), nullable=True))
    op.add_column('notifications', sa.Column('source_type', sa.String(50), nullable=True))
    op.add_column('notifications', sa.Column('source_id', sa.Integer(), nullable=True))

    # Add new enum value 'scheduled' and 'read' to notification status
    op.execute("ALTER TYPE notificationstatus ADD VALUE IF NOT EXISTS 'scheduled'")
    op.execute("ALTER TYPE notificationstatus ADD VALUE IF NOT EXISTS 'read'")

    # Add new enum values to notificationtype
    op.execute("ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'accommodation_checkin'")
    op.execute("ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'accommodation_checkout'")
    op.execute("ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'return_flight'")
    op.execute("ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'announcement'")

    # Copy body -> message for existing records
    op.execute("UPDATE notifications SET message = body WHERE message IS NULL")

    # Make message NOT NULL after data migration
    op.alter_column('notifications', 'message', nullable=False)

    # Add indexes for new columns
    op.create_index('ix_notifications_scheduled_time', 'notifications', ['scheduled_time'])
    op.create_index('ix_notifications_source_type', 'notifications', ['source_type'])

    # Drop old columns
    op.drop_column('notifications', 'body')
    op.drop_column('notifications', 'is_broadcast')
    op.drop_column('notifications', 'fcm_response')


def downgrade() -> None:
    # Reverse notifications changes
    op.add_column('notifications', sa.Column('body', sa.Text(), nullable=True))
    op.add_column('notifications', sa.Column('is_broadcast', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('notifications', sa.Column('fcm_response', sa.Text(), nullable=True))

    # Copy message -> body
    op.execute("UPDATE notifications SET body = message WHERE body IS NULL")

    op.drop_index('ix_notifications_scheduled_time', 'notifications')
    op.drop_index('ix_notifications_source_type', 'notifications')
    op.drop_index('ix_notifications_pilgrim_id', 'notifications')
    op.drop_column('notifications', 'message')
    op.drop_column('notifications', 'scheduled_time')
    op.drop_column('notifications', 'read_at')
    op.drop_column('notifications', 'delivery_mode')
    op.drop_column('notifications', 'language')
    op.drop_column('notifications', 'audio_url')
    op.drop_column('notifications', 'source_type')
    op.drop_column('notifications', 'source_id')

    # Reverse announcements changes
    op.drop_column('announcements', 'send_as_notification')
    op.drop_column('announcements', 'include_accommodation_details')
    op.drop_column('announcements', 'include_transport_details')
    op.drop_column('announcements', 'include_flight_details')
    op.drop_column('announcements', 'include_package_details')
    op.alter_column('announcements', 'message_template', new_column_name='message')
