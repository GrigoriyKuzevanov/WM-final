import asyncio
import contextlib
import logging

from fastapi_users.exceptions import UserAlreadyExists
from users.auth.user_manager import UserManager
from users.dependencies.user_manager import get_user_manager
from users.dependencies.users import get_user_db
from users.schemas import UserCreate

from core.config import settings
from core.database import db_connector

logger = logging.getLogger(__name__)

get_async_session_context = contextlib.asynccontextmanager(db_connector.get_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(user_manager: UserManager, user_create: UserCreate) -> None:
    """Creates user with given credentials in database or logs error if user with given
    email already exists.

    Args:
        user_manager (UserManager): UserManager class with users management methods
        user_create (UserCreate): Pydantic schema for create user
    """
    try:
        await user_manager.create(user_create=user_create, safe=False)
    except UserAlreadyExists:
        logger.error("User %r already exists", user_create.email)


async def create_superuser(
    email: str = settings.superuser.email,
    password: str = settings.superuser.password,
    is_active: bool = settings.superuser.is_active,
    is_superuser: bool = settings.superuser.is_superuser,
    is_verified: bool = settings.superuser.is_verified,
) -> None:
    """Creates superuser opening every context managers as the dependency manager would
    do. Uses credentials from settings by default.

    Args:
        email (str): Superuser's  email
        password (str): Superuser's password
        is_active (bool): Superuser's active status
        is_superuser (bool): Superuser's superuser status
        is_verified (bool): Superuser's verified status
    """

    user_create = UserCreate(
        email=email,
        password=password,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )
    async with get_async_session_context() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                await create_user(user_manager=user_manager, user_create=user_create)


if __name__ == "__main__":
    asyncio.run(create_superuser())
