from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_connector
from users.dependencies.fastapi_users_routes import current_user
from users.schemas import UserRead

from .adapters.role_adapter import RoleAdapter
from .adapters.structure_adapter import StructureAdapter
from .exceptions.role import AlreadyHaveRole, NotTeamAdministrator, RoleNotFoundForUser
from .exceptions.structure import StructureNotFound
from .schemas.role import RoleOut
from .schemas.structure import StructureCreate, StructureOut

router = APIRouter(
    prefix=settings.prefix.structures,
    tags=["Structures"],
)


@router.get("/my", response_model=StructureOut)
async def get_my_strucure(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    adapter = StructureAdapter(session)
    db_structure = await adapter.read_user_structure(current_user.id)

    if not db_structure:
        raise StructureNotFound

    return db_structure


@router.get("/team", response_model=list[RoleOut])
async def get_my_team(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    adapter = StructureAdapter(session)
    db_structure = await adapter.read_user_structure(current_user.id)

    if not db_structure:
        raise StructureNotFound

    return await adapter.read_structure_team(db_structure.id)


@router.post("", response_model=StructureOut, status_code=status.HTTP_201_CREATED)
async def create_structure(
    structure_input_schema: StructureCreate,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    if current_user.role_id:
        raise AlreadyHaveRole

    adapter = StructureAdapter(session)

    created_structure = await adapter.create_structure_with_admin_role(
        structure_schema=structure_input_schema,
        current_user_id=current_user.id,
    )

    return created_structure


@router.put("/my", response_model=StructureOut)
async def update_my_structure(
    structure: StructureCreate,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    structure_adapter = StructureAdapter(session)
    role_adapter = RoleAdapter(session)

    current_user_role = await role_adapter.read_item_by_id(current_user.role_id)

    if not current_user_role:
        raise RoleNotFoundForUser

    if not current_user_role.name == "Team administrator":
        raise NotTeamAdministrator

    db_structure = await structure_adapter.read_item_by_id(
        current_user_role.structure_id
    )

    return await structure_adapter.update_item(structure, db_structure)
