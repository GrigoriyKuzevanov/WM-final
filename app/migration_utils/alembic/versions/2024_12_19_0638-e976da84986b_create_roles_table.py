"""create roles table

Revision ID: e976da84986b
Revises: 4faaabf9be3c
Create Date: 2024-12-19 06:38:45.622919+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e976da84986b"
down_revision: Union[str, None] = "4faaabf9be3c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_roles")),
    )
    op.create_table(
        "roles_users_association",
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
            name=op.f("fk_roles_users_association_role_id_roles"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_roles_users_association_user_id_users"),
            ondelete="CASCADE",
        ),
    )


def downgrade() -> None:
    op.drop_table("roles_users_association")
    op.drop_table("roles")
