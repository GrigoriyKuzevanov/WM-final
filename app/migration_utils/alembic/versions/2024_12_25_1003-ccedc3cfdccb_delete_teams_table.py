"""delete teams table

Revision ID: ccedc3cfdccb
Revises: 476caf05f77d
Create Date: 2024-12-25 10:03:15.773662+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "ccedc3cfdccb"
down_revision: Union[str, None] = "476caf05f77d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("teams")


def downgrade() -> None:
    op.create_table(
        "teams",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("structure_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("info", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["structure_id"],
            ["structures.id"],
            name="fk_teams_structure_id_structures",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_teams"),
    )
