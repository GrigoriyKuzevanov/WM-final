"""create work_tasks table

Revision ID: b91b3cf0cab6
Revises: 4304879e1f63
Create Date: 2024-12-27 05:06:02.182910+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b91b3cf0cab6"
down_revision: Union[str, None] = "4304879e1f63"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "work_tasks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("comments", sa.String(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("CREATED", "IN_WORK", "COMPLETED", name="worktaskstatus"),
            nullable=False,
        ),
        sa.Column("complete_by", sa.DateTime(), nullable=False),
        sa.Column(
            "rate",
            sa.Enum("ACCEPTABLE", "GOOD", "GREAT", name="worktaskrate"),
            nullable=False,
        ),
        sa.Column("creator_id", sa.Integer(), nullable=False),
        sa.Column("assignee_id", sa.Integer(), nullable=False),
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
            ["assignee_id"], ["users.id"], name=op.f("fk_work_tasks_assignee_id_users")
        ),
        sa.ForeignKeyConstraint(
            ["creator_id"],
            ["users.id"],
            name=op.f("fk_work_tasks_creator_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_work_tasks")),
    )


def downgrade() -> None:
    op.drop_table("work_tasks")
