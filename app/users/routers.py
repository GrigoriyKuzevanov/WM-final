from fastapi import APIRouter

from core.config import settings

from .dependencies.backend import authentication_backend
from .dependencies.fastapi_users_routes import fastapi_users

router = APIRouter(
    prefix=settings.prefix.auth,
    tags=["Auth"],
)

router.include_router(
    router=fastapi_users.get_auth_router(authentication_backend),
)
