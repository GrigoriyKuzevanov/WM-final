"""change role-structures relationship to one-to-many

Revision ID: 1ade81a1c3be
Revises: 53fe6608f34f
Create Date: 2024-12-24 05:03:43.816199+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1ade81a1c3be"
down_revision: Union[str, None] = "53fe6608f34f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("roles_structures_association")
    op.add_column("roles", sa.Column("structure_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        op.f("fk_roles_structure_id_structures"),
        "roles",
        "structures",
        ["structure_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_roles_structure_id_structures"), "roles", type_="foreignkey"
    )
    op.drop_column("roles", "structure_id")
    op.create_table(
        "roles_structures_association",
        sa.Column("structure_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("role_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
            name="fk_roles_structures_association_role_id_roles",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["structure_id"],
            ["structures.id"],
            name="fk_roles_structures_association_structure_id_structures",
            ondelete="CASCADE",
        ),
    )
