import uvicorn
from admin.admin_app import admin
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from core.config import settings
from core.lifespan import lifespan

from .api_router import router as api_router

app = FastAPI(
    lifespan=lifespan,
)
app.add_middleware(SessionMiddleware, secret_key=settings.session_middleware.secret_key)

app.include_router(api_router)

admin.mount_to(app)


if __name__ == "__main__":
    uvicorn.run(
        app=settings.run.app,
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.auto_reload,
    )
