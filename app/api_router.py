from fastapi import APIRouter

from core.config import settings
from meetings.routes import router as meetings_router
from structures.relations_routes import router as relations_router
from structures.roles_routes import router as roles_router
from structures.structures_routes import router as structures_router
from users.auth_routes import router as auth_router
from users.users_routes import router as users_router

router = APIRouter(
    prefix=settings.prefix.api_prefix,
)

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(structures_router)
router.include_router(roles_router)
router.include_router(relations_router)
router.include_router(meetings_router)
