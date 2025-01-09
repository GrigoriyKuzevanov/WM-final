from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_connector
from users.dependencies.fastapi_users_routes import current_user
from users.schemas import UserRead

from .adapters.relation_adapter import RelationAdapter
from .adapters.role_adapter import RoleAdapter
from .dependencies.role import current_user_team_admin
from .schemas.realtion import RelationCreate, RelationOut
from .schemas.role import RoleOut
from .services.relation import RelationService
from .services.role import RoleService

router = APIRouter(
    prefix=settings.prefix.relations,
    tags=["Relations"],
)


@router.post(
    "/",
    response_model=RelationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new relation",
    description="""
    Creates a new relation using the provided schema. Requires authorization.

    Requirements:
    - The current user must be a team administrator
    - The superior role and the subordinate role must exist
    - The superior role, the subordinate role and the current user role must belong to
    the same structure
    - The relation must be unique
    """,
)
async def create_relation(
    relation_input_schema: RelationCreate,
    current_user_team_admin: RoleOut = Depends(current_user_team_admin),
    session: AsyncSession = Depends(db_connector.get_session),
):
    roles_adapter = RoleAdapter(session)
    relations_adapter = RelationAdapter(session)

    relations_service = RelationService(relations_adapter)

    return await relations_service.create_relation(
        roles_adapter=roles_adapter,
        relation_create_schema=relation_input_schema,
        structure_id=current_user_team_admin.structure_id,
    )


@router.delete(
    "/{relation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a relation",
    description="""
    Deletes a relation with provided id. Requires authorization.

    Parameters:
    - relation_id: The id of the relation to delete

    Requirements:
    - A relation with provided id must exist
    - The current user must be the relation's team administrator
    """,
)
async def delete_relation(
    relation_id: int,
    current_user_team_admin: RoleOut = Depends(current_user_team_admin),
    session: AsyncSession = Depends(db_connector.get_session),
):
    relations_adapter = RelationAdapter(session)

    relations_service = RelationService(relations_adapter)

    await relations_service.delete_relation(
        relation_id, current_user_team_admin.structure_id
    )


@router.get(
    "/me-subordinate",
    response_model=list[RelationOut],
    summary="Get relations where current user is subordinate",
    description="""
    Retrieves all relations where the current user role is subordinate. Requires
    authorization.

    Requirements:
    - The current user must have a role
    """,
)
async def get_me_subordinate(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    roles_adapter = RoleAdapter(session)

    roles_service = RoleService(roles_adapter)

    return await roles_service.get_role_subordinates(current_user.role_id)


@router.get(
    "/me-superior",
    response_model=list[RelationOut],
    summary="Get relations where current user is superior",
    description="""
    Retrieves all relations where the current user role is superior. Requires
    authorization.

    Requirements:
    - The current user must have a role
    """,
)
async def get_me_superior(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    roles_adapter = RoleAdapter(session)

    roles_service = RoleService(roles_adapter)

    return await roles_service.get_role_superiors(current_user.role_id)
