import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request

from core.models.base_model import Base

if TYPE_CHECKING:
    from users.models import User


association_table = Table(
    "meetings_users_association",
    Base.metadata,
    Column("meeting_id", ForeignKey("meetings.id")),
    Column("user_id", ForeignKey("users.id")),
)


class Meeting(Base):
    __tablename__ = "meetings"

    topic: Mapped[str] = mapped_column(nullable=False)
    info: Mapped[str]
    meet_datetime: Mapped[datetime.datetime]
    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    users: Mapped[list["User"]] = relationship(
        secondary=association_table, back_populates="meetings"
    )
    creator: Mapped["User"] = relationship(back_populates="created_meetings")

    async def __admin_repr__(self, request: Request) -> str:
        """Model's representation in admin.

        Args:
            request (_type_): Request instance

        Returns:
            str: Model's string representation
        """

        return f"{self.topic}, {self.meet_datetime}"
