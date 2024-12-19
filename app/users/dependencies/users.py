from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_connector
from users.models import User


async def get_user_db(
    session: AsyncSession = Depends(db_connector.get_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    """Provides initialized database adapter of User model.

    Args:
        session (AsyncSession): Async database session.
    """

    yield User.get_db(session=session)
