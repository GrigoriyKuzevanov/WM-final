from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base_model import Base


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[int]):
    """A class for representation access_tokens table in the database.

    Attributes:
        user_id (Mapped[int]): Id of the associated user.
    """

    __tablename__ = "access_tokens"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    @classmethod
    def get_db(cls, session: AsyncSession) -> SQLAlchemyAccessTokenDatabase:
        """Provides database adapter for access token model.

        Args:
            session (AsyncSession): Async database session to connect

        Returns:
            SQLAlchemyAccessTokenDatabase: Fastapi-users sqlalchemy adapter for access
            token model
        """

        return SQLAlchemyAccessTokenDatabase(session, cls)
