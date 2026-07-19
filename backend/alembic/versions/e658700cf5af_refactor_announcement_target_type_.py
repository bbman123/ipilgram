"""refactor announcement target_type target_id

Revision ID: e658700cf5af
Revises: 2812a65ef19e
Create Date: 2026-07-18 23:13:51.375082
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'e658700cf5af'
down_revision: Union[str, None] = '2812a65ef19e'
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


def upgrade() -> None:
    target_type_enum = postgresql.ENUM(
        'all', 'pilgrim', 'package', 'flight', 'accommodation', 'transport',
        name='targettype', create_type=False
    )
    target_type_enum.create(op.get_bind(), checkfirst=True)

    _add_column_if_not_exists('announcements', sa.Column('target_type', target_type_enum, nullable=False, server_default='all'))
    _add_column_if_not_exists('announcements', sa.Column('target_id', sa.Integer(), nullable=True))
    _drop_index_if_exists('ix_announcements_category', 'announcements')
    _drop_index_if_exists('ix_announcements_priority', 'announcements')
    _drop_column_if_exists('announcements', 'language')
    _drop_column_if_exists('announcements', 'category')

    _create_index_if_not_exists('ix_announcements_target_type', 'announcements', ['target_type'], unique=False)
    _create_index_if_not_exists('ix_announcements_priority', 'announcements', ['priority'], unique=False)


def downgrade() -> None:
    _drop_index_if_exists('ix_announcements_priority', 'announcements')
    _drop_index_if_exists('ix_announcements_target_type', 'announcements')

    category_enum = postgresql.ENUM(
        'emergency', 'general', 'flight', 'accommodation', 'transport',
        name='announcementcategory', create_type=False
    )
    category_enum.create(op.get_bind(), checkfirst=True)

    _add_column_if_not_exists('announcements', sa.Column('category', category_enum, nullable=False, server_default='general'))
    _add_column_if_not_exists('announcements', sa.Column('language', sa.VARCHAR(length=10), nullable=False, server_default='en'))
    _create_index_if_not_exists('ix_announcements_category', 'announcements', ['category'], unique=False)
    _create_index_if_not_exists('ix_announcements_priority', 'announcements', ['priority'], unique=False)

    _drop_column_if_exists('announcements', 'target_id')
    _drop_column_if_exists('announcements', 'target_type')
