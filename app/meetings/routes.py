from fastapi import APIRouter

from core.config import settings

router = APIRouter(
    prefix=settings.prefix.meetings,
    tags=["Meetings"],
)
