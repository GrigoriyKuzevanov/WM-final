import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request

from core.models.base_model import Base

if TYPE_CHECKING:
    from users.models import User


class WorkTaskStatus(Enum):
    """Enum class for work task statuses."""

    CREATED = "created"
    IN_WORK = "in_work"
    COMPLETED = "completed"


class WorkTaskRate(Enum):
    """Enum class for work tasks rates."""

    ACCEPTABLE = 1
    GOOD = 2
    GREAT = 3


class WorkTask(Base):
    """A class for represtation work_tasks table in the database."""

    __tablename__ = "work_tasks"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    comments: Mapped[str]
    status: Mapped[WorkTaskStatus] = mapped_column(
        default=WorkTaskStatus.CREATED, nullable=False
    )
    complete_by: Mapped[datetime.datetime] = mapped_column(nullable=False)
    rate: Mapped[WorkTaskRate]
    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    creator: Mapped["User"] = relationship(back_populates="created_work_tasks")
    assignee: Mapped["User"] = relationship(back_populates="assigned_work_tasks")

    async def __admin_repr__(self, request: Request) -> str:
        """Model's representation in admin.

        Args:
            request (_type_): Request instance

        Returns:
            str: Model's string representation
        """

        return f"{self.name}, {self.complete_by}"
