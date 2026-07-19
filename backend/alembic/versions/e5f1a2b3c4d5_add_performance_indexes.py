"""add_performance_indexes

Revision ID: e5f1a2b3c4d5
Revises: c8866b59a4b6
Create Date: 2026-07-18 16:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = 'e5f1a2b3c4d5'
down_revision: Union[str, None] = 'c8866b59a4b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Flights: index on pilgrim_id for JOIN performance and status for filtering
    op.create_index('ix_flights_pilgrim_id', 'flights', ['pilgrim_id'])
    op.create_index('ix_flights_status', 'flights', ['status'])
    op.create_index('ix_flights_departure_datetime', 'flights', ['departure_datetime'])

    # Accommodations: index on pilgrim_id and city for filtering
    op.create_index('ix_accommodations_pilgrim_id', 'accommodations', ['pilgrim_id'])
    op.create_index('ix_accommodations_city', 'accommodations', ['city'])

    # Transports: index on pilgrim_id and transport_type for filtering
    op.create_index('ix_transports_pilgrim_id', 'transports', ['pilgrim_id'])
    op.create_index('ix_transports_transport_type', 'transports', ['transport_type'])
    op.create_index('ix_transports_pickup_time', 'transports', ['pickup_time'])

    # Announcements: index on category, priority for filtering
    op.create_index('ix_announcements_category', 'announcements', ['category'])
    op.create_index('ix_announcements_priority', 'announcements', ['priority'])

    # Preferences: index on pilgrim_id (unique already, but explicit for query performance)
    op.create_index('ix_preferences_pilgrim_id', 'preferences', ['pilgrim_id'])

    # Notifications: index on pilgrim_id, notification_type, status for filtering
    op.create_index('ix_notifications_pilgrim_id', 'notifications', ['pilgrim_id'])
    op.create_index('ix_notifications_notification_type', 'notifications', ['notification_type'])
    op.create_index('ix_notifications_status', 'notifications', ['status'])

    # Device tokens: index on pilgrim_id for JOIN performance
    op.create_index('ix_device_tokens_pilgrim_id', 'device_tokens', ['pilgrim_id'])


def downgrade() -> None:
    op.drop_index('ix_device_tokens_pilgrim_id', table_name='device_tokens')
    op.drop_index('ix_notifications_status', table_name='notifications')
    op.drop_index('ix_notifications_notification_type', table_name='notifications')
    op.drop_index('ix_notifications_pilgrim_id', table_name='notifications')
    op.drop_index('ix_preferences_pilgrim_id', table_name='preferences')
    op.drop_index('ix_announcements_priority', table_name='announcements')
    op.drop_index('ix_announcements_category', table_name='announcements')
    op.drop_index('ix_transports_pickup_time', table_name='transports')
    op.drop_index('ix_transports_transport_type', table_name='transports')
    op.drop_index('ix_transports_pilgrim_id', table_name='transports')
    op.drop_index('ix_accommodations_city', table_name='accommodations')
    op.drop_index('ix_accommodations_pilgrim_id', table_name='accommodations')
    op.drop_index('ix_flights_departure_datetime', table_name='flights')
    op.drop_index('ix_flights_status', table_name='flights')
    op.drop_index('ix_flights_pilgrim_id', table_name='flights')
