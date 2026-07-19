"""add missing performance indexes

Revision ID: f1a2b3c4d5e6
Revises: e658700cf5af
Create Date: 2026-07-19 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'f1a2b3c4d5e6'
down_revision: Union[str, None] = 'e658700cf5af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _create_index_if_not_exists(index_name, table_name, columns):
    bind = op.get_bind()
    insp = sa.inspect(bind)
    existing = [idx['name'] for idx in insp.get_indexes(table_name)]
    if index_name not in existing:
        op.create_index(index_name, table_name, columns, unique=False)


def upgrade() -> None:
    _create_index_if_not_exists('ix_users_package_id', 'users', ['package_id'])
    _create_index_if_not_exists('ix_packages_flight_id', 'packages', ['flight_id'])
    _create_index_if_not_exists('ix_packages_accommodation_id', 'packages', ['accommodation_id'])
    _create_index_if_not_exists('ix_packages_transport_id', 'packages', ['transport_id'])
    _create_index_if_not_exists('ix_announcements_target_type', 'announcements', ['target_type'])
    _create_index_if_not_exists('ix_announcements_publish_date', 'announcements', ['publish_date'])
    _create_index_if_not_exists('ix_announcements_expiry_date', 'announcements', ['expiry_date'])
    _create_index_if_not_exists('ix_device_tokens_pilgrim_id', 'device_tokens', ['pilgrim_id'])
    _create_index_if_not_exists('ix_notifications_pilgrim_id', 'notifications', ['pilgrim_id'])


def downgrade() -> None:
    op.drop_index('ix_notifications_pilgrim_id', table_name='notifications')
    op.drop_index('ix_device_tokens_pilgrim_id', table_name='device_tokens')
    op.drop_index('ix_announcements_expiry_date', table_name='announcements')
    op.drop_index('ix_announcements_publish_date', table_name='announcements')
    op.drop_index('ix_announcements_target_type', table_name='announcements')
    op.drop_index('ix_packages_transport_id', table_name='packages')
    op.drop_index('ix_packages_accommodation_id', table_name='packages')
    op.drop_index('ix_packages_flight_id', table_name='packages')
    op.drop_index('ix_users_package_id', table_name='users')
