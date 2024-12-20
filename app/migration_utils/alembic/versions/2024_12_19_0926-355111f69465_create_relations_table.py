"""create relations table

Revision ID: 355111f69465
Revises: dd0bd41c92fd
Create Date: 2024-12-19 09:26:15.446021+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "355111f69465"
down_revision: Union[str, None] = "dd0bd41c92fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "relations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("superior_id", sa.Integer(), nullable=False),
        sa.Column("subordinate_id", sa.Integer(), nullable=False),
        sa.Column("structure_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["structure_id"],
            ["structures.id"],
            name=op.f("fk_relations_structure_id_structures"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["subordinate_id"],
            ["roles.id"],
            name=op.f("fk_relations_subordinate_id_roles"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["superior_id"],
            ["roles.id"],
            name=op.f("fk_relations_superior_id_roles"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_relations")),
        sa.UniqueConstraint(
            "superior_id", "subordinate_id", "structure_id", name="uq_role_hierarchy"
        ),
    )


def downgrade() -> None:
    op.drop_table("relations")
