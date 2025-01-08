from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_connector
from users.dependencies.fastapi_users_routes import current_user
from users.schemas import UserRead

from .adapters.relation_adapter import RelationAdapter
from .adapters.role_adapter import RoleAdapter
from .dependencies.role import current_user_role, current_user_team_admin
from .schemas.realtion import RelationCreate, RelationOut
from .schemas.role import RoleOut
from .services.relation import RelationService
from .services.role import RoleService

router = APIRouter(
    prefix=settings.prefix.relations,
    tags=["Relations"],
)


@router.post("/", response_model=RelationOut, status_code=status.HTTP_201_CREATED)
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


@router.get("/me-subordinate", response_model=list[RelationOut])
async def get_me_subordinate(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    roles_adapter = RoleAdapter(session)

    roles_service = RoleService(roles_adapter)

    return await roles_service.get_role_subordinates(current_user.role_id)


@router.get("/me-superior", response_model=list[RelationOut])
async def get_me_superior(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    roles_adapter = RoleAdapter(session)

    roles_service = RoleService(roles_adapter)

    return await roles_service.get_role_superiors(current_user.role_id)
