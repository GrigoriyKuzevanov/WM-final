from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request

from core.models.base_model import Base
from meetings.models import association_table

if TYPE_CHECKING:
    from meetings.models import Meeting
    from structures.models.role import Role
    from work_tasks.models import WorkTask


class User(Base, SQLAlchemyBaseUserTable[int]):
    """A class for represtation users table in the database."""

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(length=60))
    last_name: Mapped[str] = mapped_column(String(length=60))
    info: Mapped[str] = mapped_column(nullable=True)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="SET NULL"), nullable=True
    )

    role: Mapped["Role"] = relationship(back_populates="users")
    meetings: Mapped[list["Meeting"]] = relationship(
        secondary=association_table, back_populates="users"
    )
    created_meetings: Mapped[list["Meeting"]] = relationship(
        back_populates="creator",
        cascade="all, delete",
    )
    created_work_tasks: Mapped[list["WorkTask"]] = relationship(
        foreign_keys="WorkTask.creator_id",
        back_populates="creator",
        cascade="all, delete",
    )
    assigned_work_tasks: Mapped[list["WorkTask"]] = relationship(
        foreign_keys="WorkTask.assignee_id", back_populates="assignee"
    )

    async def __admin_repr__(self, request: Request) -> str:
        """Model's representation in admin.

        Args:
            request (_type_): Request instance

        Returns:
            str: Model's string representation
        """

        return f"{self.email}"

    @classmethod
    def get_db(cls, session: AsyncSession) -> SQLAlchemyUserDatabase:
        """Provides database adapter for user model.

        Args:
            session (AsyncSession): Async database session to connect

        Returns:
            SQLAlchemyUserDatabase: Fastapi-users sqlalchemy adapter for user model
        """

        return SQLAlchemyUserDatabase(session, cls)
