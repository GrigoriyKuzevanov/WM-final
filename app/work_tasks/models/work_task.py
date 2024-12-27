import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request

from core.models.base_model import Base

if TYPE_CHECKING:
    from users.models import User


class WorkTask(Base):
    """A class for represtation work_tasks table in the database."""

    __tablename__ = "work_tasks"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    comments: Mapped[str]
    status: Mapped[str] = mapped_column(String(34), nullable=False)
    complete_by: Mapped[datetime.datetime] = mapped_column(nullable=False)
    rate: Mapped[int] = mapped_column(nullable=False)
    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    creator: Mapped["User"] = relationship(
        foreign_keys=[creator_id], back_populates="created_work_tasks"
    )
    assignee: Mapped["User"] = relationship(
        foreign_keys=[assignee_id], back_populates="assigned_work_tasks"
    )

    async def __admin_repr__(self, request: Request) -> str:
        """Model's representation in admin.

        Args:
            request (Request): Request instance

        Returns:
            str: Model's string representation
        """

        return f"{self.name}, {self.complete_by}"
