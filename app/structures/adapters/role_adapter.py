from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

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
        """Bounds user to the role.

        Args:
            user_id (int): User id

        Returns:
            RM: Updated role object
        """

        user = await self.session.get(User, user_id)
        self.model.users.append(user)

        await self.session.commit()
        await self.session.refresh(self.model)

        return self.model

    async def get_with_subordinates(self, role_id: int) -> RM:
        """Gets Role with provided id with joined loaded suboridinates.

        Args:
            role_id (int): Role id

        Returns:
            RM: Role object
        """

        stmt = (
            select(Role)
            .options(joinedload(Role.subordinates))
            .where(Role.id == role_id)
        )

        return await self.session.scalar(stmt)

    async def get_with_superiors(self, role_id: int) -> RM:
        """Gets Role with provided id with joined loaded get_with_superiors.

        Args:
            role_id (int): Role id

        Returns:
            RM: Role object
        """

        stmt = (
            select(Role).options(joinedload(Role.superiors)).where(Role.id == role_id)
        )

        return await self.session.scalar(stmt)
