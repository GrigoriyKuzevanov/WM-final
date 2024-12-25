from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from structures.models import Role, Structure
from structures.schemas.role import RoleCreate
from structures.schemas.structure import StructureCreate
from users.models import User

from .model_adapter import ModelAdapter

SM = TypeVar("SM", bound=Structure)


class StructureAdapter(ModelAdapter):
    """Adapter class for performing database operations to the Structure model."""

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the adapter

        Args:
            session (AsyncSession): Async session
        """

        super().__init__(Structure, session)

    async def read_user_structure(self, user_id: int) -> SM | None:
        """Retrieves the structure associated with a specific user through his role.

        Args:
            user_id (int): Id of the user

        Returns:
            SM | None: Structure object from the db or None if not found
        """

        stmt = (
            select(Structure)
            .join(Role, Role.structure_id == Structure.id)
            .join(User, User.role_id == Role.id)
            .where(User.id == user_id)
        )

        return await self.session.scalar(stmt)

    async def create_structure_with_admin_role(
        self, structure_schema: StructureCreate, current_user_id: int
    ) -> SM:
        """Creates a new structure. Also creates a new "Team administrator" role
        associated with current user and created structure.

        Args:
            structure_schema (StructureCreate): Pydantic schema containing structure
            data
            current_user_id (int): Current user id

        Returns:
            SM: Created structure object from db
        """

        structure = self.model(**structure_schema.model_dump())

        self.session.add(structure)
        await self.session.flush()

        role_create_schema = RoleCreate(
            name="Team administrator",
            info="Creator of the structure",
            structure_id=structure.id,
        )

        role = Role(**role_create_schema.model_dump())
        user = await self.session.get(User, current_user_id)
        role.users.append(user)

        self.session.add(role)
        await self.session.flush()

        await self.session.commit()

        return structure
