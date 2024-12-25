from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base
from structures.models import Role
from users.models import User

from .model_adapter import ModelAdapter


class RoleAdapter(ModelAdapter):
    def __init__(self, session: AsyncSession):
        self.model = Role
        self.session = session

    async def add_user(self, user_id: int) -> Role:
        user = await self.session.get(User, user_id)
        self.model.users.append(user)

        await self.session.commit()
        await self.session.refresh(self.model)

        return self.model
