from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.model_adapter import ModelAdapter
from structures.models import Role
from structures.schemas.role import RoleCreate
from users.models import User


class RoleAdapter(ModelAdapter):
    """Adapter class for performing database operations to the Team model."""

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the adapter

        Args:
            session (AsyncSession): Async session
        """

        super().__init__(Role, session)

    async def create_role(
        self, role_create_schema: RoleCreate, structure_id: int
    ) -> Role:
        """Creates a new role with provided structure id.

        Args:
            role_create_schema (RoleCreate): Pydantic schema to create role
            structure_id (int): Structure id

        Returns:
            Role: Created role object
        """

        role = self.model(**role_create_schema.model_dump(), structure_id=structure_id)

        self.session.add(role)
        await self.session.commit()

        return role

    async def bound_user(self, role: Role, user: User) -> Role:
        """Bound user to role.

        Args:
            role (Role): Role object
            user (User): User object

        Returns:
            Role: Role object with bounded user
        """

        role.users.append(user)

        self.session.add(role)
        await self.session.commit()

        return role

    async def get_with_users(self, role_id: int) -> Role:
        """Gets Role with provided id with joined loaded users.

        Args:
            role_id (int): Role id

        Returns:
            Role: Role object
        """

        stmt = select(Role).options(joinedload(Role.users)).where(Role.id == role_id)

        return await self.session.scalar(stmt)

    async def get_with_subordinates(self, role_id: int) -> Role:
        """Gets Role with provided id with joined loaded suboridinates.

        Args:
            role_id (int): Role id

        Returns:
            Role: Role object
        """

        stmt = (
            select(Role)
            .options(joinedload(Role.subordinates))
            .where(Role.id == role_id)
        )

        return await self.session.scalar(stmt)

    async def get_with_superiors(self, role_id: int) -> Role:
        """Gets Role with provided id with joined loaded get_with_superiors.

        Args:
            role_id (int): Role id

        Returns:
            Role: Role object
        """

        stmt = (
            select(Role).options(joinedload(Role.superiors)).where(Role.id == role_id)
        )

        return await self.session.scalar(stmt)
