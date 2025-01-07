from structures.adapters.role_adapter import RoleAdapter
from structures.exceptions.role import RoleNotFound
from structures.models import Role


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
            role_id (int): It of the role

        Raises:
            RoleNotFound: Http exception

        Returns:
            Role: Role model
        """

        role = await self.roles_adapter.read_item_by_id(role_id)

        if not role:
            raise RoleNotFound

        return role
