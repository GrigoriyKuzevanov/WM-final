from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.model_adapter import ModelAdapter
from core.models import db_connector
from users.dependencies.fastapi_users_routes import current_user
from users.models import User
from users.schemas import UserRead

from .adapters.role_adapter import RoleAdapter
from .dependencies.role import current_user_role
from .exceptions.role import (
    DeleteOtherTeamRole,
    DeleteYourselfRole,
    NotTeamAdministrator,
    RoleNotFoundForUser,
)
from .schemas.role import RoleCreate, RoleOut, RoleUpdate

router = APIRouter(
    prefix=settings.prefix.roles,
    tags=["Roles"],
)


@router.get("/my", response_model=RoleOut)
async def get_my_role(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    adapter = RoleAdapter(session)

    if not current_user.role_id:
        raise RoleNotFoundForUser

    return await adapter.read_item_by_id(current_user.role_id)


@router.post("/{user_id}", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
async def create_role(
    user_id: int,
    role_input_schema: RoleCreate,
    current_user_role: RoleOut = Depends(current_user_role),
    session: AsyncSession = Depends(db_connector.get_session),
):
    role_adapter = RoleAdapter(session)
    user_adapter = ModelAdapter(User, session)

    if not current_user_role.name == "Team administrator":
        raise NotTeamAdministrator

    user = await user_adapter.read_item_by_id(user_id)

    return await role_adapter.create_role_and_bound_to_user(
        role_create_schema=role_input_schema,
        user_to_bound=user,
        structure_id=current_user_role.structure_id,
    )


@router.put("/my", response_model=RoleOut)
async def update_my_role(
    role_input_schema: RoleUpdate,
    current_user_role: RoleOut = Depends(current_user_role),
    session: AsyncSession = Depends(db_connector.get_session),
):
    role_adapter = RoleAdapter(session)

    return await role_adapter.update_item(role_input_schema, current_user_role)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    current_user_role: RoleOut = Depends(current_user_role),
    session: AsyncSession = Depends(db_connector.get_session),
):
    if current_user_role.id == role_id:
        raise DeleteYourselfRole

    adapter = RoleAdapter(session)

    if not current_user_role.name == "Team administrator":
        raise NotTeamAdministrator

    role_to_delete = await adapter.read_item_by_id(role_id)

    if not role_to_delete:
        raise RoleNotFoundForUser

    if not current_user_role.structure_id == role_to_delete.structure_id:
        raise DeleteOtherTeamRole

    await adapter.delete_item(role_to_delete)
