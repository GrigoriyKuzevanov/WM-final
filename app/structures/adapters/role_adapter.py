from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from structures.models import Role
from users.models import User

from .model_adapter import ModelAdapter

RM = TypeVar("RM", bound=Role)


class RoleAdapter(ModelAdapter):
    """Adapter class for performing database operations to the Team model."""

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the adapter

        Args:
            session (AsyncSession): Async session
        """

        super().__init__(Role, session)

    async def add_user(self, user_id: int) -> RM:
        """Bound user to the role.

        Args:
            user_id (int): User id

        Returns:
            Role: Updated role object
        """

        user = await self.session.get(User, user_id)
        self.model.users.append(user)

        await self.session.commit()
        await self.session.refresh(self.model)

        return self.model
