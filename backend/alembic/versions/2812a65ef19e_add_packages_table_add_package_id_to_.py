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


def _create_table_if_not_exists(table_name, *args, **kwargs):
    bind = op.get_bind()
    insp = sa.inspect(bind)
    if table_name not in insp.get_table_names():
        op.create_table(table_name, *args, **kwargs)


def _drop_table_if_exists(table_name):
    bind = op.get_bind()
    insp = sa.inspect(bind)
    if table_name in insp.get_table_names():
        op.drop_table(table_name)


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


def _drop_constraint_if_exists(constraint_name, table_name, type_):
    bind = op.get_bind()
    insp = sa.inspect(bind)
    for fk in insp.get_foreign_keys(table_name):
        if fk['name'] == constraint_name:
            op.drop_constraint(constraint_name, table_name, type_=type_)
            return
    for uq in insp.get_unique_constraints(table_name):
        if uq['name'] == constraint_name:
            op.drop_constraint(constraint_name, table_name, type_=type_)
            return


def upgrade() -> None:
    _create_table_if_not_exists('packages',
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

    _drop_constraint_if_exists('accommodations_pilgrim_id_fkey', 'accommodations', 'foreignkey')
    _drop_column_if_exists('accommodations', 'pilgrim_id')
    _drop_constraint_if_exists('flights_pilgrim_id_fkey', 'flights', 'foreignkey')
    _drop_column_if_exists('flights', 'pilgrim_id')
    _drop_constraint_if_exists('transports_pilgrim_id_fkey', 'transports', 'foreignkey')
    _drop_column_if_exists('transports', 'pilgrim_id')

    _add_column_if_not_exists('users', sa.Column('package_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'packages', ['package_id'], ['id'], ondelete='SET NULL')


def downgrade() -> None:
    op.drop_constraint(None, 'users', type_='foreignkey')
    _drop_column_if_exists('users', 'package_id')

    _add_column_if_not_exists('transports', sa.Column('pilgrim_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('transports_pilgrim_id_fkey', 'transports', 'users', ['pilgrim_id'], ['id'], ondelete='CASCADE')

    _add_column_if_not_exists('flights', sa.Column('pilgrim_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('flights_pilgrim_id_fkey', 'flights', 'users', ['pilgrim_id'], ['id'], ondelete='CASCADE')

    _add_column_if_not_exists('accommodations', sa.Column('pilgrim_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('accommodations_pilgrim_id_fkey', 'accommodations', 'users', ['pilgrim_id'], ['id'], ondelete='CASCADE')

    _drop_table_if_exists('packages')
