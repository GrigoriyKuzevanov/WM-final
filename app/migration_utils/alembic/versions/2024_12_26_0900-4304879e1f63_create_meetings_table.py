"""create meetings table

Revision ID: 4304879e1f63
Revises: ccedc3cfdccb
Create Date: 2024-12-26 09:00:05.397563+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4304879e1f63"
down_revision: Union[str, None] = "ccedc3cfdccb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "meetings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("topic", sa.String(), nullable=False),
        sa.Column("info", sa.String(), nullable=False),
        sa.Column("meet_datetime", sa.DateTime(), nullable=False),
        sa.Column("creator_id", sa.Integer(), nullable=False),
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
            ["creator_id"],
            ["users.id"],
            name=op.f("fk_meetings_creator_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_meetings")),
    )
    op.create_table(
        "meetings_users_association",
        sa.Column("meeting_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["meeting_id"],
            ["meetings.id"],
            name=op.f("fk_meetings_users_association_meeting_id_meetings"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_meetings_users_association_user_id_users"),
        ),
    )


def downgrade() -> None:
    op.drop_table("meetings_users_association")
    op.drop_table("meetings")
