from fastapi_users.authentication import AuthenticationBackend

from users.auth import bearer_transport

from .strategy import get_database_strategy, get_redis_strategy

authentication_backend = AuthenticationBackend(
    name="access-tokens-db",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)


redis_authentication_backend = AuthenticationBackend(
    name="access-tokens-redis",
    transport=bearer_transport,
    get_strategy=get_redis_strategy,
)
