from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_connector
from users.dependencies.fastapi_users_routes import current_user
from users.schemas import UserRead

from .adapters.structure_adapter import StructureAdapter
from .dependencies.role import current_user_team_admin
from .schemas.role import RoleOut
from .schemas.structure import StructureCreate, StructureOut, StructureUpdate
from .services.structure import StructureService

router = APIRouter(
    prefix=settings.prefix.structures,
    tags=["Structures"],
)


@router.get(
    "/me",
    response_model=StructureOut,
    summary="Get a user's structure",
    description="""
    Retrieves a structure of the current user. Requires authorization.

    Requirements:
    - The current user must be bound to a structure
    """,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "The current user unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The current user is not bound to any structure"
        },
    },
)
async def get_my_strucure(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    structures_adapter = StructureAdapter(session)

    structures_service = StructureService(structures_adapter)

    return await structures_service.get_user_structure(current_user.id)


@router.get(
    "/team",
    response_model=list[RoleOut],
    summary="Get user's team",
    description="""
    Retrieves a list of the roles of the current user's structure. Requires
    authorization.

    Requirements:
    - The current user must be bound to a structure
    """,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "The current user unauthorized",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The current user is not bound to any structure"
        },
    },
)
async def get_my_team(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    structures_adapter = StructureAdapter(session)

    structures_service = StructureService(structures_adapter)

    return await structures_service.get_user_team(current_user.id)


@router.post(
    "",
    response_model=StructureOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new structure",
    description="""
    Creates a new structure by a provided schema. Also creates a new admin role for the
    created structure and bound it to the current user. Requires authorization.

    Requirements:
    - The current user must not have a role
    """,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "The current user unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "The current user already has a role"
        },
    },
)
async def create_structure(
    structure_input_schema: StructureCreate,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    structures_adapter = StructureAdapter(session)

    structures_service = StructureService(structures_adapter)

    return await structures_service.create_structure(
        structure_create_schema=structure_input_schema,
        team_admin=current_user,
    )


@router.put(
    "/me",
    response_model=StructureOut,
    summary="Update a user's structure",
    description="""
    Updates the current user's structure with a provided schema. Requires authorization.

    Requirements:
    - The current user must be a team administrator
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
async def update_my_structure(
    structure_input_schema: StructureUpdate,
    current_user_team_admin: RoleOut = Depends(current_user_team_admin),
    session: AsyncSession = Depends(db_connector.get_session),
):
    structures_adapter = StructureAdapter(session)

    structures_service = StructureService(structures_adapter)

    return await structures_service.update_structure(
        structure_update_schema=structure_input_schema,
        structure_id=current_user_team_admin.structure_id,
    )
