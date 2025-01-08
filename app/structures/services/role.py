from core.model_adapter import ModelAdapter
from structures.adapters.role_adapter import RoleAdapter
from structures.exceptions.role import (
    DeleteOtherTeamRole,
    DeleteYourselfRole,
    RoleNotFound,
    RoleNotFoundForUser,
)
from structures.models import Role
from structures.schemas.role import RoleCreate, RoleOut, RoleUpdate


class RoleService:
    """Roles managing service."""

    def __init__(self, roles_adapter: RoleAdapter) -> None:
        """Inits RoleService.

        Args:
            roles_adapter (RoleAdapter): Adapter to interacting with database
        """

        self.roles_adapter = roles_adapter

    async def get_role_by_id(self, role_id: int) -> Role:
        """Retrieves role by id.

        Args:
            role_id (int): Id of the role

        Raises:
            RoleNotFound: Http exception

        Returns:
            Role: Role model
        """

        role = await self.roles_adapter.read_item_by_id(role_id)

        if not role:
            raise RoleNotFound

        return role

    async def get_role_subordinates(self, role_id: int) -> list[Role]:
        """Retrieves role's subordinates.

        Args:
            role_id (int): Id of the role

        Raises:
            RoleNotFound: Http exception

        Returns:
            list[Role]: List of subordinates roles
        """

        role = await self.roles_adapter.get_with_subordinates(role_id)

        if not role:
            raise RoleNotFound

        return role.subordinates

    async def create_role(
        self,
        current_user_role: RoleOut,
        role_create_schema: RoleCreate,
        user_id: int,
        user_adapter: ModelAdapter,
    ) -> Role:
        """Create new role and bound it to provided user.

        Args:
            current_user_role (RoleOut): Current user role schema
            role_create_schema (RoleCreate): Schema to create new role
            user_id (int): Id of the user to bound
            user_adapter (ModelAdapter): Adapter for interactive with database to
            retrieve user model

        Returns:
            Role: Created role model
        """

        user = await user_adapter.read_item_by_id(user_id)

        return await self.roles_adapter.create_role_and_bound_to_user(
            role_create_schema=role_create_schema,
            user_to_bound=user,
            structure_id=current_user_role.structure_id,
        )

    async def update_role(
        self, role_update_schema: RoleUpdate, role_to_update: Role
    ) -> Role:
        """Update role model.

        Args:
            role_update_schema (RoleUpdate): Schema to update role
            role_to_update (Role): Role model to update

        Returns:
            Role: Updated role model
        """

        return await self.roles_adapter.update_item(
            update_schema=role_update_schema, item=role_to_update
        )

    async def delete_role(self, role_id: int, current_user_role: RoleOut) -> None:
        """Deletes role by provided role id.

        Args:
            role_id (int): Id of the role to delete
            current_user_role (RoleOut): Current user role schema

        Raises:
            DeleteYourselfRole: If try to delete current user's role
            RoleNotFoundForUser: If role to delete not found
            DeleteOtherTeamRole: If try to delete role of not current user's structure
        """

        if current_user_role.id == role_id:
            raise DeleteYourselfRole

        role_to_delete = await self.roles_adapter.read_item_by_id(role_id)

        if not role_to_delete:
            raise RoleNotFoundForUser

        if not current_user_role.structure_id == role_to_delete.structure_id:
            raise DeleteOtherTeamRole

        await self.roles_adapter.delete_item(role_to_delete)
