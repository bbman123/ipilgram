"""normalize delivery mode enum values

Revision ID: 0002
Revises: 0001
Create Date: 2026-08-03 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()

    # Normalize delivery_mode values: "Text + Audio" → "TextPlusAudio"
    bind.execute(sa.text(
        "UPDATE preferences SET delivery_mode = 'TextPlusAudio' WHERE delivery_mode = 'Text + Audio'"
    ))


def downgrade() -> None:
    bind = op.get_bind()

    # Revert delivery_mode normalization
    bind.execute(sa.text(
        "UPDATE preferences SET delivery_mode = 'Text + Audio' WHERE delivery_mode = 'TextPlusAudio'"
    ))
