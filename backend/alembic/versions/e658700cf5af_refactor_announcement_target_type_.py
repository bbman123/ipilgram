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


def upgrade() -> None:
    target_type_enum = postgresql.ENUM(
        'all', 'pilgrim', 'package', 'flight', 'accommodation', 'transport',
        name='targettype', create_type=False
    )
    target_type_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('announcements', sa.Column('target_type', target_type_enum, nullable=False, server_default='all'))
    op.add_column('announcements', sa.Column('target_id', sa.Integer(), nullable=True))
    op.drop_index('ix_announcements_category', table_name='announcements')
    op.drop_index('ix_announcements_priority', table_name='announcements')
    op.drop_column('announcements', 'language')
    op.drop_column('announcements', 'category')

    op.create_index('ix_announcements_target_type', 'announcements', ['target_type'], unique=False)
    op.create_index('ix_announcements_priority', 'announcements', ['priority'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_announcements_priority', table_name='announcements')
    op.drop_index('ix_announcements_target_type', table_name='announcements')

    category_enum = postgresql.ENUM(
        'emergency', 'general', 'flight', 'accommodation', 'transport',
        name='announcementcategory', create_type=False
    )
    category_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('announcements', sa.Column('category', category_enum, nullable=False, server_default='general'))
    op.add_column('announcements', sa.Column('language', sa.VARCHAR(length=10), nullable=False, server_default='en'))
    op.create_index('ix_announcements_category', 'announcements', ['category'], unique=False)
    op.create_index('ix_announcements_priority', 'announcements', ['priority'], unique=False)

    op.drop_column('announcements', 'target_id')
    op.drop_column('announcements', 'target_type')
