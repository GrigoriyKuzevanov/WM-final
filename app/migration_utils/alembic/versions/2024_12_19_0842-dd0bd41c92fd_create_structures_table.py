"""create structures table

Revision ID: dd0bd41c92fd
Revises: e976da84986b
Create Date: 2024-12-19 08:42:05.648011+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dd0bd41c92fd"
down_revision: Union[str, None] = "e976da84986b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "structures",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_structures")),
    )
    op.create_table(
        "roles_structures_association",
        sa.Column("structure_id", sa.Integer(), nullable=True),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
            name=op.f("fk_roles_structures_association_role_id_roles"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["structure_id"],
            ["structures.id"],
            name=op.f("fk_roles_structures_association_structure_id_structures"),
            ondelete="CASCADE",
        ),
    )


def downgrade() -> None:
    op.drop_table("roles_structures_association")
    op.drop_table("structures")
