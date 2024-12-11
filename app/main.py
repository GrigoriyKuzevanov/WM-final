import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.lifespan import lifespan

app = FastAPI(
    lifespan=lifespan,
)


if __name__ == "__main__":
    uvicorn.run(
        app=settings.run.app,
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.auto_reload,
    )
