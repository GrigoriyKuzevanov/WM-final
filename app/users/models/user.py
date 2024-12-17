from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    """A class for represtation users table in the database"""

    __tablename__ = "users"

    @classmethod
    def get_db(cls, session: AsyncSession) -> SQLAlchemyUserDatabase:
        """Provides database adapter for user model.

        Args:
            session (AsyncSession): Async database session to connect

        Returns:
            SQLAlchemyUserDatabase: Fastapi-users sqlalchemy adapter for user model
        """

        return SQLAlchemyUserDatabase(session, cls)
