from fastapi import APIRouter
from users.routers import router as auth_router

from core.config import settings

router = APIRouter(
    prefix=settings.prefix.api_prefix,
    tags=["Auth"],
)

router.include_router(auth_router)
