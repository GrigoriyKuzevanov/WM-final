from structures.adapters.structure_adapter import StructureAdapter
from structures.exceptions.role import AlreadyHaveRole
from structures.exceptions.structure import StructureNotFound
from structures.models import Role, Structure
from structures.schemas.structure import StructureCreate, StructureUpdate
from users.schemas.user import UserRead


class StructureService:
    """Structures managing service."""

    def __init__(self, structures_adapter: StructureAdapter) -> None:
        """Inits StructureService.

        Args:
            structures_adapter (StructureAdapter): Adapter to interacting with database
        """

        self.structures_adapter = structures_adapter

    async def get_user_structure(self, user_id: int) -> Structure:
        """Retrieve structure by provided user id.

        Args:
            user_id (int): User id

        Raises:
            StructureNotFound: If structure not found for user

        Returns:
            Structure: Structure model
        """

        structure = await self.structures_adapter.read_user_structure(user_id)

        if not structure:
            raise StructureNotFound

        return structure

    async def get_user_team(self, user_id: int) -> list[Role]:
        """Retrieve user's structure team.

        Args:
            user_id (int): User id

        Returns:
            list[Role]: List of structure's roles
        """

        structure = await self.get_user_structure(user_id)

        if not structure:
            raise StructureNotFound

        return await self.structures_adapter.read_structure_team(structure.id)

    async def create_structure(
        self,
        structure_create_schema: StructureCreate,
        team_admin: UserRead,
    ) -> Structure:
        """Creates a new structure with provided admin.

        Args:
            structure_create_schema (StructureCreate): Structure schema to create
            team_admin (UserRead): User schema to create admin role

        Raises:
            AlreadyHaveRole: If user alaready have role

        Returns:
            Structure: Created structure model
        """

        if team_admin.role_id:
            raise AlreadyHaveRole

        return await self.structures_adapter.create_structure_with_admin_role(
            structure_schema=structure_create_schema,
            current_user_id=team_admin.id,
        )

    async def update_structure(
        self, structure_update_schema: StructureUpdate, structure_id: int
    ) -> Structure:
        """Updates structure by provided structure id.

        Args:
            structure_update_schema (StructureUpdate): Structure schema to update
            structure_id (int): Structure id to update

        Returns:
            Structure: Updated structure model
        """

        structure = await self.structures_adapter.read_item_by_id(structure_id)

        return await self.structures_adapter.update_item(
            update_schema=structure_update_schema,
            item=structure,
        )
