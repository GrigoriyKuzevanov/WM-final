from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_connector
from users.models import AccessToken


async def get_access_token_db(
    session: AsyncSession = Depends(db_connector.get_session),
) -> AsyncGenerator[SQLAlchemyAccessTokenDatabase, None]:
    """Provides initialized database adapter of Access Token model.

    Args:
        session (AsyncSession): Async database session.
    """

    yield AccessToken.get_db(session=session)
