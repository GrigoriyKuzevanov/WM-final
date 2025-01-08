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


@router.get("/my", response_model=RoleOut)
async def get_my_role(current_user_role: RoleOut = Depends(current_user_role)):
    return current_user_role


@router.post("/{user_id}", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
async def create_role(
    user_id: int,
    role_input_schema: RoleCreate,
    current_user_team_admin: RoleOut = Depends(current_user_team_admin),
    session: AsyncSession = Depends(db_connector.get_session),
):
    roles_adapter = RoleAdapter(session)
    user_adapter = ModelAdapter(User, session)

    role_service = RoleService(roles_adapter)

    return await role_service.create_role(
        current_user_role=current_user_team_admin,
        role_create_schema=role_input_schema,
        user_id=user_id,
        user_adapter=user_adapter,
    )


@router.put("/my", response_model=RoleOut)
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


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
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
