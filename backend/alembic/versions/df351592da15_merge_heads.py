"""merge_heads

Revision ID: df351592da15
Revises: a1b2c3d4e5f6, b1c2d3e4f5a6
Create Date: 2026-07-19 16:48:05.372416
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = 'df351592da15'
down_revision: Union[str, None] = ('a1b2c3d4e5f6', 'b1c2d3e4f5a6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
