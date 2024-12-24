"""add info field to teams, roles, stuctures tables

Revision ID: 53fe6608f34f
Revises: f994564ffbe6
Create Date: 2024-12-24 04:46:02.716789+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "53fe6608f34f"
down_revision: Union[str, None] = "f994564ffbe6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("roles", sa.Column("info", sa.String(), nullable=False))
    op.add_column("structures", sa.Column("info", sa.String(), nullable=False))
    op.add_column("teams", sa.Column("info", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("teams", "info")
    op.drop_column("structures", "info")
    op.drop_column("roles", "info")
