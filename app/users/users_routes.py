from fastapi import APIRouter

from core.config import settings

from .dependencies.fastapi_users_routes import fastapi_users
from .schemas import UserRead, UserUpdate

router = APIRouter(
    prefix=settings.prefix.users,
    tags=["Users"],
)

# /me
# /{id}
router.include_router(router=fastapi_users.get_users_router(UserRead, UserUpdate))
