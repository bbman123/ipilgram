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
    # Flights: index on pilgrim_id for JOIN performance and status for filtering
    _create_index_if_not_exists('ix_flights_pilgrim_id', 'flights', ['pilgrim_id'])
    _create_index_if_not_exists('ix_flights_status', 'flights', ['status'])
    _create_index_if_not_exists('ix_flights_departure_datetime', 'flights', ['departure_datetime'])

    # Accommodations: index on pilgrim_id and city for filtering
    _create_index_if_not_exists('ix_accommodations_pilgrim_id', 'accommodations', ['pilgrim_id'])
    _create_index_if_not_exists('ix_accommodations_city', 'accommodations', ['city'])

    # Transports: index on pilgrim_id and transport_type for filtering
    _create_index_if_not_exists('ix_transports_pilgrim_id', 'transports', ['pilgrim_id'])
    _create_index_if_not_exists('ix_transports_transport_type', 'transports', ['transport_type'])
    _create_index_if_not_exists('ix_transports_pickup_time', 'transports', ['pickup_time'])

    # Announcements: index on category, priority for filtering
    _create_index_if_not_exists('ix_announcements_category', 'announcements', ['category'])
    _create_index_if_not_exists('ix_announcements_priority', 'announcements', ['priority'])

    # Preferences: index on pilgrim_id (unique already, but explicit for query performance)
    _create_index_if_not_exists('ix_preferences_pilgrim_id', 'preferences', ['pilgrim_id'])

    # Notifications: index on pilgrim_id, notification_type, status for filtering
    _create_index_if_not_exists('ix_notifications_pilgrim_id', 'notifications', ['pilgrim_id'])
    _create_index_if_not_exists('ix_notifications_notification_type', 'notifications', ['notification_type'])
    _create_index_if_not_exists('ix_notifications_status', 'notifications', ['status'])

    # Device tokens: index on pilgrim_id for JOIN performance
    _create_index_if_not_exists('ix_device_tokens_pilgrim_id', 'device_tokens', ['pilgrim_id'])


def downgrade() -> None:
    _drop_index_if_exists('ix_device_tokens_pilgrim_id', 'device_tokens')
    _drop_index_if_exists('ix_notifications_status', 'notifications')
    _drop_index_if_exists('ix_notifications_notification_type', 'notifications')
    _drop_index_if_exists('ix_notifications_pilgrim_id', 'notifications')
    _drop_index_if_exists('ix_preferences_pilgrim_id', 'preferences')
    _drop_index_if_exists('ix_announcements_priority', 'announcements')
    _drop_index_if_exists('ix_announcements_category', 'announcements')
    _drop_index_if_exists('ix_transports_pickup_time', 'transports')
    _drop_index_if_exists('ix_transports_transport_type', 'transports')
    _drop_index_if_exists('ix_transports_pilgrim_id', 'transports')
    _drop_index_if_exists('ix_accommodations_city', 'accommodations')
    _drop_index_if_exists('ix_accommodations_pilgrim_id', 'accommodations')
    _drop_index_if_exists('ix_flights_departure_datetime', 'flights')
    _drop_index_if_exists('ix_flights_status', 'flights')
    _drop_index_if_exists('ix_flights_pilgrim_id', 'flights')
