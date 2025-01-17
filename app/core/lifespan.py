from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from core.models import db_connector
from core.redis import redis_connector


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manages the fastapi application's lifespan handling startup and shutdown events.

    on startup:

    on shutdown:
        1) closes redis connection
        2) closes database connection

    Args:
        app (FastAPI): The FastAPI application instance

    Returns:
        AsyncGenerator[None, None]: AsyncGenerator using by FastAPI
    """

    yield

    await redis_connector.close_connection()
    await db_connector.dispose()
