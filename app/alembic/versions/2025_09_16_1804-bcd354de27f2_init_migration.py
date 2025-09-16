"""Init migration

Revision ID: bcd354de27f2
Revises:
Create Date: 2025-09-16 18:04:21.260276

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "bcd354de27f2"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
