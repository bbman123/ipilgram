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


def _add_column_if_not_exists(table_name, column):
    bind = op.get_bind()
    insp = sa.inspect(bind)
    existing = [c['name'] for c in insp.get_columns(table_name)]
    if column.name not in existing:
        op.add_column(table_name, column)


def _drop_column_if_exists(table_name, column_name):
    bind = op.get_bind()
    insp = sa.inspect(bind)
    existing = [c['name'] for c in insp.get_columns(table_name)]
    if column_name in existing:
        op.drop_column(table_name, column_name)


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
    bind = op.get_bind()
    insp = sa.inspect(bind)

    # === ANNOUNCEMENTS: rename message -> message_template, add new columns ===
    ann_cols = [c['name'] for c in insp.get_columns('announcements')]
    if 'message' in ann_cols and 'message_template' not in ann_cols:
        op.alter_column('announcements', 'message', new_column_name='message_template')
    _add_column_if_not_exists('announcements', sa.Column('include_package_details', sa.Boolean(), server_default='false', nullable=False))
    _add_column_if_not_exists('announcements', sa.Column('include_flight_details', sa.Boolean(), server_default='false', nullable=False))
    _add_column_if_not_exists('announcements', sa.Column('include_transport_details', sa.Boolean(), server_default='false', nullable=False))
    _add_column_if_not_exists('announcements', sa.Column('include_accommodation_details', sa.Boolean(), server_default='false', nullable=False))
    _add_column_if_not_exists('announcements', sa.Column('send_as_notification', sa.Boolean(), server_default='false', nullable=False))

    # === NOTIFICATIONS: redesign columns ===
    _add_column_if_not_exists('notifications', sa.Column('message', sa.Text(), nullable=True))
    _add_column_if_not_exists('notifications', sa.Column('scheduled_time', sa.DateTime(timezone=True), nullable=True))
    _add_column_if_not_exists('notifications', sa.Column('read_at', sa.DateTime(timezone=True), nullable=True))
    _add_column_if_not_exists('notifications', sa.Column('delivery_mode', sa.String(20), nullable=True))
    _add_column_if_not_exists('notifications', sa.Column('language', sa.String(20), nullable=True))
    _add_column_if_not_exists('notifications', sa.Column('audio_url', sa.String(500), nullable=True))
    _add_column_if_not_exists('notifications', sa.Column('source_type', sa.String(50), nullable=True))
    _add_column_if_not_exists('notifications', sa.Column('source_id', sa.Integer(), nullable=True))

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
    notif_cols = [c['name'] for c in insp.get_columns('notifications')]
    msg_nullable = True
    for c in insp.get_columns('notifications'):
        if c['name'] == 'message':
            msg_nullable = c['nullable']
            break
    if msg_nullable:
        op.alter_column('notifications', 'message', nullable=False)

    # Add indexes for new columns
    _create_index_if_not_exists('ix_notifications_scheduled_time', 'notifications', ['scheduled_time'])
    _create_index_if_not_exists('ix_notifications_source_type', 'notifications', ['source_type'])

    # Drop old columns
    _drop_column_if_exists('notifications', 'body')
    _drop_column_if_exists('notifications', 'is_broadcast')
    _drop_column_if_exists('notifications', 'fcm_response')


def downgrade() -> None:
    # Reverse notifications changes
    _add_column_if_not_exists('notifications', sa.Column('body', sa.Text(), nullable=True))
    _add_column_if_not_exists('notifications', sa.Column('is_broadcast', sa.Boolean(), server_default='false', nullable=False))
    _add_column_if_not_exists('notifications', sa.Column('fcm_response', sa.Text(), nullable=True))

    # Copy message -> body
    op.execute("UPDATE notifications SET body = message WHERE body IS NULL")

    _drop_index_if_exists('ix_notifications_scheduled_time', 'notifications')
    _drop_index_if_exists('ix_notifications_source_type', 'notifications')
    _drop_index_if_exists('ix_notifications_pilgrim_id', 'notifications')
    _drop_column_if_exists('notifications', 'message')
    _drop_column_if_exists('notifications', 'scheduled_time')
    _drop_column_if_exists('notifications', 'read_at')
    _drop_column_if_exists('notifications', 'delivery_mode')
    _drop_column_if_exists('notifications', 'language')
    _drop_column_if_exists('notifications', 'audio_url')
    _drop_column_if_exists('notifications', 'source_type')
    _drop_column_if_exists('notifications', 'source_id')

    # Reverse announcements changes
    _drop_column_if_exists('announcements', 'send_as_notification')
    _drop_column_if_exists('announcements', 'include_accommodation_details')
    _drop_column_if_exists('announcements', 'include_transport_details')
    _drop_column_if_exists('announcements', 'include_flight_details')
    _drop_column_if_exists('announcements', 'include_package_details')

    bind = op.get_bind()
    insp = sa.inspect(bind)
    ann_cols = [c['name'] for c in insp.get_columns('announcements')]
    if 'message_template' in ann_cols and 'message' not in ann_cols:
        op.alter_column('announcements', 'message_template', new_column_name='message')
