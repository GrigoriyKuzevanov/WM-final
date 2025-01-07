from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_connector
from users.dependencies.fastapi_users_routes import current_user
from users.schemas import UserRead

from .adapters.relation_adapter import RelationAdapter
from .adapters.role_adapter import RoleAdapter
from .exceptions.role import NotTeamAdministrator, RoleNotFound, RoleNotFoundForUser
from .schemas.realtion import RelationCreate, RelationOut

router = APIRouter(
    prefix=settings.prefix.relations,
    tags=["Relations"],
)


@router.post("/", response_model=RelationOut, status_code=status.HTTP_201_CREATED)
async def create_relation(
    relation_input_schema: RelationCreate,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    role_adapter = RoleAdapter(session)
    relation_adapter = RelationAdapter(session)

    current_user_role = await role_adapter.read_item_by_id(current_user.role_id)

    if not current_user_role:
        raise RoleNotFoundForUser

    if not current_user_role.name == "Team administrator":
        raise NotTeamAdministrator

    if not await role_adapter.read_item_by_id(
        relation_input_schema.superior_id
    ) or not await role_adapter.read_item_by_id(relation_input_schema.subordinate_id):
        raise RoleNotFound

    return await relation_adapter.create_realtion_with_users_structure_id(
        relation_input_schema, current_user_role.structure_id
    )


@router.get("/me-subordinate", response_model=list[RelationOut])
async def get_me_subordinate(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    role_adapter = RoleAdapter(session)

    current_user_role = await role_adapter.get_with_subordinates(current_user.role_id)

    if not current_user_role:
        raise RoleNotFoundForUser

    return current_user_role.subordinates


@router.get("/me-superior", response_model=list[RelationOut])
async def get_me_superior(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    role_adapter = RoleAdapter(session)

    current_user_role = await role_adapter.get_with_superiors(current_user.role_id)

    if not current_user_role:
        raise RoleNotFoundForUser

    return current_user_role.superiors
