from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import settings


class DataBaseConnector:
    """A class to manage connection to database using SQLAlchemy async engine."""

    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        """Inits the database connector with given parameters.

        Args:
            url (str): Url to connect the db
            echo (bool): Logging sql statesments. "True" by default
            echo_pool (bool): Logging connection pool information. "True" by default
            pool_size (int): The number of connections to keep open inside the
            connection pool. 5 by default
            max_overflow (int): The number of connections to allow in connection pool
            overflow. 10 by default
        """

        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        """Closes engine connection to the database."""

        await self.engine.dispose()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Provides an async database session.

        Yields:
            AsyncSession: An active async database session
        """

        async with self.session_factory() as session:
            yield session


db_connector = DataBaseConnector(
    url=settings.main_pg_db.postgres_url.unicode_string(),
    echo=settings.main_pg_db.echo_sql,
    echo_pool=settings.main_pg_db.echo_pool,
    pool_size=settings.main_pg_db.pool_size,
    max_overflow=settings.main_pg_db.max_overflow,
)
