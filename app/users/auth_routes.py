from fastapi import APIRouter

from core.config import settings

from .dependencies.backend import authentication_backend
from .dependencies.fastapi_users_routes import fastapi_users
from .schemas import UserCreate, UserRead

router = APIRouter(
    prefix=settings.prefix.auth,
    tags=["Auth"],
)

# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(authentication_backend),
)


# /register
router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),
)
