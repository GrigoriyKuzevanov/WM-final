from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, relationship

from core.models.base_model import Base
from structures.models.role import association_table

if TYPE_CHECKING:
    from structures.models.role import Role


class User(Base, SQLAlchemyBaseUserTable[int]):
    """A class for represtation users table in the database"""

    __tablename__ = "users"

    roles: Mapped[list["Role"]] = relationship(
        secondary=association_table, back_populates="users", cascade="all, delete"
    )

    @classmethod
    def get_db(cls, session: AsyncSession) -> SQLAlchemyUserDatabase:
        """Provides database adapter for user model.

        Args:
            session (AsyncSession): Async database session to connect

        Returns:
            SQLAlchemyUserDatabase: Fastapi-users sqlalchemy adapter for user model
        """

        return SQLAlchemyUserDatabase(session, cls)
