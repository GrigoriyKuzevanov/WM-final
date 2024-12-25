"""change user-role relationship to one-to-many

Revision ID: 476caf05f77d
Revises: 1ade81a1c3be
Create Date: 2024-12-24 11:31:12.572285+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "476caf05f77d"
down_revision: Union[str, None] = "1ade81a1c3be"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("roles_users_association")
    op.add_column("users", sa.Column("role_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f("fk_users_role_id_roles"),
        "users",
        "roles",
        ["role_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_users_role_id_roles"), "users", type_="foreignkey")
    op.drop_column("users", "role_id")
    op.create_table(
        "roles_users_association",
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("role_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
            name="fk_roles_users_association_role_id_roles",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_roles_users_association_user_id_users",
            ondelete="CASCADE",
        ),
    )
