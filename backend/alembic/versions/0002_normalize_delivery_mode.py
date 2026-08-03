"""no-op: delivery mode normalization is handled at the application layer

The DB stores 'Text + Audio' which matches DeliveryMode.TextPlusAudio.value.
The DeliveryModeType adapter converts it correctly on read.
Pydantic validators normalize input on write.

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
    pass


def downgrade() -> None:
    pass
