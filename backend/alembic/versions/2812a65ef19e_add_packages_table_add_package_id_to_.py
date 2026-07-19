"""add_packages_table_add_package_id_to_users_remove_pilgrim_id_from_flights_accommodations_transports

Revision ID: 2812a65ef19e
Revises: e5f1a2b3c4d5
Create Date: 2026-07-18 16:56:41.723384
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = '2812a65ef19e'
down_revision: Union[str, None] = 'e5f1a2b3c4d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('packages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('flight_id', sa.Integer(), nullable=True),
    sa.Column('accommodation_id', sa.Integer(), nullable=True),
    sa.Column('transport_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.String(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.String(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['accommodation_id'], ['accommodations.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['transport_id'], ['transports.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )

    op.drop_constraint('accommodations_pilgrim_id_fkey', 'accommodations', type_='foreignkey')
    op.drop_column('accommodations', 'pilgrim_id')
    op.drop_constraint('flights_pilgrim_id_fkey', 'flights', type_='foreignkey')
    op.drop_column('flights', 'pilgrim_id')
    op.drop_constraint('transports_pilgrim_id_fkey', 'transports', type_='foreignkey')
    op.drop_column('transports', 'pilgrim_id')

    op.add_column('users', sa.Column('package_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'packages', ['package_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'package_id')

    op.add_column('transports', sa.Column('pilgrim_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('transports_pilgrim_id_fkey', 'transports', 'users', ['pilgrim_id'], ['id'], ondelete='CASCADE')

    op.add_column('flights', sa.Column('pilgrim_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('flights_pilgrim_id_fkey', 'flights', 'users', ['pilgrim_id'], ['id'], ondelete='CASCADE')

    op.add_column('accommodations', sa.Column('pilgrim_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('accommodations_pilgrim_id_fkey', 'accommodations', 'users', ['pilgrim_id'], ['id'], ondelete='CASCADE')

    op.drop_table('packages')
