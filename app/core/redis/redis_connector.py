from redis.asyncio import Redis

from core.config import settings


class RedisConnector:
    """A class to manage connection to Redis database."""

    def __init__(self, host: str, port: int, db: int, password: str, user: str) -> None:
        """Inits Redis client.

        Args:
            host (str): host to connect
            port (int): port to connect
            db (int): db to connect
            password (str): password
            user (str): username
        """

        self._redis = Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            username=user,
        )

    def get_client(self) -> Redis:
        """Returns connected Redis client.

        Returns:
            Redis: Redis client
        """

        return self._redis

    async def close_connection(self) -> None:
        """Closes Redis connection."""

        await self._redis.close()


redis_connector = RedisConnector(
    host=settings.redis.host,
    port=settings.redis.port,
    db=settings.redis.db,
    user=settings.redis.user,
    password=settings.redis.password,
)
