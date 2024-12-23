"""update User model

Revision ID: f994564ffbe6
Revises: 49057828b860
Create Date: 2024-12-23 12:48:21.402961+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f994564ffbe6"
down_revision: Union[str, None] = "49057828b860"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("name", sa.String(length=60), nullable=False))
    op.add_column("users", sa.Column("last_name", sa.String(length=60), nullable=False))
    op.add_column("users", sa.Column("info", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "info")
    op.drop_column("users", "last_name")
    op.drop_column("users", "name")
