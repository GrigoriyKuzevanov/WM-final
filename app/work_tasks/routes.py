from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.model_adapter import ModelAdapter
from core.models import db_connector
from structures.adapters.relation_adapter import RelationAdapter
from structures.adapters.role_adapter import RoleAdapter
from structures.dependencies.role import current_user_role
from structures.schemas.role import RoleOut
from users.dependencies.fastapi_users_routes import current_user
from users.models import User
from users.schemas import UserRead

from .adapters.work_task_adapter import WorkTaskAdapter
from .schemas import (
    WorkTaskCreate,
    WorkTaskOut,
    WorkTaskUpdate,
    WorkTaskUpdateRate,
    WorkTaskUpdateStatus,
)
from .service import WorkTaskService

router = APIRouter(
    prefix=settings.prefix.work_tasks,
    tags=["Work Tasks"],
)


@router.post("", response_model=WorkTaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_input_schema: WorkTaskCreate,
    current_user: UserRead = Depends(current_user),
    current_user_role: RoleOut = Depends(current_user_role),
    session: AsyncSession = Depends(db_connector.get_session),
):
    tasks_adapter = WorkTaskAdapter(session)
    roles_adapter = RoleAdapter(session)
    users_adapter = ModelAdapter(User, session)
    relations_adapter = RelationAdapter(session)

    tasks_service = WorkTaskService(tasks_adapter)

    return await tasks_service.create_task(
        user_id=current_user.id,
        user_role_id=current_user_role.id,
        task_create_schema=task_input_schema,
        users_adapter=users_adapter,
        roles_adapter=roles_adapter,
        relations_adapter=relations_adapter,
    )


@router.put("/{task_id}", response_model=WorkTaskOut)
async def update_task(
    task_id: int,
    task_input_schema: WorkTaskUpdate,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    tasks_adapter = WorkTaskAdapter(session)

    tasks_service = WorkTaskService(tasks_adapter)

    return await tasks_service.update_task(
        task_id=task_id,
        user_id=current_user.id,
        task_update_schema=task_input_schema,
    )


@router.patch("/{task_id}/status", response_model=WorkTaskOut)
async def update_task_status(
    task_id: int,
    task_input_schema: WorkTaskUpdateStatus,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    tasks_adapter = WorkTaskAdapter(session)

    tasks_service = WorkTaskService(tasks_adapter)

    return await tasks_service.update_task_status(
        task_id=task_id,
        user_id=current_user.id,
        task_update_schema=task_input_schema,
    )


@router.patch("/{task_id}/rate", response_model=WorkTaskOut)
async def update_task_rate(
    task_id: int,
    task_input_schema: WorkTaskUpdateRate,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    tasks_adapter = WorkTaskAdapter(session)

    tasks_service = WorkTaskService(tasks_adapter)

    return await tasks_service.update_task_rate(
        task_id=task_id,
        user_id=current_user.id,
        task_update_schema=task_input_schema,
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    tasks_adapter = WorkTaskAdapter(session)

    tasks_service = WorkTaskService(tasks_adapter)

    await tasks_service.delete_task(task_id=task_id, user_id=current_user.id)


@router.get("/rating/me")
async def get_my_rating(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    tasks_adapter = WorkTaskAdapter(session)

    tasks_service = WorkTaskService(tasks_adapter)

    return await tasks_service.get_user_rating(user_id=current_user.id)


@router.get("/rating/team")
async def get_team_rating(
    current_user_role: RoleOut = Depends(current_user_role),
    session: AsyncSession = Depends(db_connector.get_session),
):
    tasks_adapter = WorkTaskAdapter(session)

    tasks_service = WorkTaskService(tasks_adapter)

    return await tasks_service.get_team_rating(
        structure_id=current_user_role.structure_id
    )
