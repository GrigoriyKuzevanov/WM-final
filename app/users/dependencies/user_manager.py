from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase

from users.auth.user_manager import UserManager

from .users import get_user_db


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    """Provides initialized fastapi-user UserManager object.

    Args:
        user_db: Initialized database adapter of User model.
    """

    yield UserManager(user_db)
