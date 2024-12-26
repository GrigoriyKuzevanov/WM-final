from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from structures.models import Role
from structures.schemas.role import RoleCreate
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

    async def create_role_and_bound_to_user(
        self, role_create_schema: RoleCreate, user_to_bound: User, structure_id: int
    ) -> RM:
        """Creates new role and bounds created role to current user.

        Args:
            role_create_schema (RoleCreate): Pydantic schema to create role
            current_user_id (int): Current user id to bound

        Returns:
            RM: Created role object
        """

        role = self.model(**role_create_schema.model_dump(), structure_id=structure_id)

        role.users.append(user_to_bound)

        self.session.add(role)
        await self.session.commit()

        return role

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
