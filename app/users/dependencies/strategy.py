from fastapi import Depends
from fastapi_users.authentication import RedisStrategy
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy,
)

from core.config import settings
from core.redis import redis_connector
from users.models import AccessToken

from .access_tokens import get_access_token_db


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    """Provides DatabaseStrategy instance for handling access tokens.

    Args:
        access_token_db (AccessTokenDatabase[AccessToken]): Unitialized database adapter
        of Access Token model

    Returns:
        DatabaseStrategy: The strategy for managing access token
    """

    return DatabaseStrategy(
        access_token_db, lifetime_seconds=settings.access_token.lifetime_seconds
    )


def get_redis_strategy() -> RedisStrategy:
    """Provides RedisStrategy instance for handling access tokens.

    Returns:
        RedisStrategy: The strategy for managing access token
    """

    return RedisStrategy(
        redis=redis_connector.get_client(),
        lifetime_seconds=settings.access_token.lifetime_seconds,
    )
