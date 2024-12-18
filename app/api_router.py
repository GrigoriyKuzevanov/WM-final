from fastapi import APIRouter
from users.auth_routes import router as auth_router
from users.users_routes import router as users_router

from core.config import settings

router = APIRouter(
    prefix=settings.prefix.api_prefix,
)

router.include_router(auth_router)
router.include_router(users_router)
