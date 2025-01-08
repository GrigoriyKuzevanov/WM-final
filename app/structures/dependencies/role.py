from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_connector
from structures.adapters.role_adapter import RoleAdapter
from structures.exceptions.role import NotTeamAdministrator
from structures.models import Role
from structures.services.role import RoleService
from users.dependencies.fastapi_users_routes import current_user
from users.schemas import UserRead


async def current_user_role(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
) -> Role:
    """Fetches current user role.

    Args:
        current_user (UserRead): Current authenticated user
        session (AsyncSession): Database session

    Returns:
        Role: Role model associated with current user
    """

    role_service = RoleService(roles_adapter=RoleAdapter(session=session))

    return await role_service.get_role_by_id(current_user.role_id)


async def current_user_team_admin(
    current_user_role: Role = Depends(current_user_role),
) -> Role:
    """Fetches current user role if it's a team administrator

    Args:
        current_user_role (Role): Current user role

    Raises:
        NotTeamAdministrator: if current user role is not team admin

    Returns:
        Role: Role model associated with current user
    """

    team_admin_name = "Team administrator"

    if not current_user_role.name == team_admin_name:
        raise NotTeamAdministrator

    return current_user_role
