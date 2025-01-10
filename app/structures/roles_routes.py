from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.model_adapter import ModelAdapter
from core.models import db_connector
from users.models import User

from .adapters.role_adapter import RoleAdapter
from .dependencies.role import current_user_role, current_user_team_admin
from .models.role import Role
from .schemas.role import RoleCreate, RoleOut, RoleUpdate
from .services.role import RoleService

router = APIRouter(
    prefix=settings.prefix.roles,
    tags=["Roles"],
)


@router.get(
    "/my",
    response_model=RoleOut,
    summary="Get a user's role",
    description="""
    Retrieves a role of the current user. Requires authorization.

    Requirements:
    - The current user must have a role
    """,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "The current user unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The current user doesn't have a role",
        },
    },
)
async def get_my_role(current_user_role: RoleOut = Depends(current_user_role)):
    return current_user_role


@router.post(
    "",
    response_model=RoleOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new role",
    description="""
    Creates a new role by a provided schema. Requires authorization. The created role
    belongs to the current user role's structure.

    Requirements:
    - The current user must be the team administrator
    """,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "The current user unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "The current user is not a team administrator",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The current user doesn't have a role",
        },
    },
)
async def create_role(
    role_input_schema: RoleCreate,
    current_user_team_admin: RoleOut = Depends(current_user_team_admin),
    session: AsyncSession = Depends(db_connector.get_session),
):
    roles_adapter = RoleAdapter(session)

    role_service = RoleService(roles_adapter)

    return await role_service.create_role(
        role_create_schema=role_input_schema,
        structure_id=current_user_team_admin.structure_id,
    )


@router.get(
    "/{role_id}/bound-user/{user_id}",
    response_model=RoleOut,
    summary="Bound a user to a role",
    description="""
    Bounds a user with provided id to a role with provided id. Requires authorization.

    Parameters:
    - role_id: The id of the role which need bound to user
    - user_id: The id of the user to bound to the role

    Requirements:
    - The current user must be the team administrator
    - The role with provided id must exist
    - The role with provided id and the current user must belong to the same structure
    - The user with provided id must exist
    """,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "The current user unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": """The current user is not a team administrator;
                              Can't bound a user to a role from another structure""",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": """The current user doesn't have a role;
                              A role with provided id isn't found;
                              A user with provided id isn't found""",
        },
    },
)
async def bound_user(
    role_id: int,
    user_id: int,
    current_user_team_admin: RoleOut = Depends(current_user_team_admin),
    session: AsyncSession = Depends(db_connector.get_session),
):
    roles_adapter = RoleAdapter(session)
    users_adapter = ModelAdapter(User, session)

    roles_service = RoleService(roles_adapter)

    return await roles_service.bound_user(
        role_id=role_id,
        structure_id=current_user_team_admin.structure_id,
        user_id=user_id,
        users_adapter=users_adapter,
    )


@router.put(
    "/my",
    response_model=RoleOut,
    summary="Update a user's role",
    description="""
    Updates the current user's role with provided schema. Requires authorization.

    Requirements:
    - The current user must have a role
    """,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "The current user unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The current user doesn't have a role",
        },
    },
)
async def update_my_role(
    role_input_schema: RoleUpdate,
    current_user_role: Role = Depends(current_user_role),
    session: AsyncSession = Depends(db_connector.get_session),
):
    roles_adapter = RoleAdapter(session)

    role_service = RoleService(roles_adapter)

    return await role_service.update_role(
        role_update_schema=role_input_schema, role_to_update=current_user_role
    )


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a role",
    description="""
    Deletes a role with provided id. Requires authorization.

    Parameters:
    - role_id: The id of the role to delete

    Requirements:
    - The current user must be a team administrator
    - The role with provided id must exist
    - The role with provided id must not be the current user's role
    - The role with provided id must belong to the current user's structure
    """,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "The current user unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": """The current user is not a team administrator;
                              Trying delete own role;
                              Can't delete a role from another structure""",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": """The current user doesn't have a role;
                              A role with provided id isn't found""",
        },
    },
)
async def delete_role(
    role_id: int,
    current_user_team_admin: RoleOut = Depends(current_user_team_admin),
    session: AsyncSession = Depends(db_connector.get_session),
):
    roles_adapter = RoleAdapter(session)

    role_service = RoleService(roles_adapter)

    await role_service.delete_role(
        role_id=role_id, current_user_role=current_user_team_admin
    )
