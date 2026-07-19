"""fix timestamp columns from varchar to timestamp

Revision ID: a1b2c3d4e5f6
Revises: f1a2b3c4d5e6
Create Date: 2026-07-19 01:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'f1a2b3c4d5e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLES = [
    "users", "flights", "accommodations", "transports",
    "packages", "announcements", "preferences", "notifications",
    "device_tokens",
]


def upgrade() -> None:
    for table in TABLES:
        for col in ("created_at", "updated_at"):
            op.alter_column(
                table, col,
                type_=sa.DateTime(timezone=True),
                postgresql_using=f"{col}::timestamp with time zone",
                server_default=sa.func.now(),
            )
    op.alter_column(
        "notifications", "sent_at",
        type_=sa.DateTime(timezone=True),
        nullable=True,
        postgresql_using="sent_at::timestamp with time zone",
    )
    op.alter_column(
        "refresh_tokens", "expires_at",
        type_=sa.DateTime(timezone=True),
        postgresql_using="expires_at::timestamp with time zone",
    )


def downgrade() -> None:
    for table in TABLES:
        for col in ("created_at", "updated_at"):
            op.alter_column(table, col, type_=sa.String(), server_default=None)
