from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.model_adapter import ModelAdapter
from core.models import db_connector
from structures.adapters.relation_adapter import RelationAdapter
from structures.adapters.role_adapter import RoleAdapter
from structures.exceptions.role import RoleNotFoundForUser
from users.dependencies.fastapi_users_routes import current_user
from users.models import User
from users.schemas import UserRead
from utils.check_time import check_datetime_after_now

from .adapters.work_task_adapter import WorkTaskAdapter
from .exceptions import (
    NotTaskAssignee,
    NotTaskCreator,
    TaskBeforeNow,
    TaskForThisUser,
    TasksNotFound,
)
from .schemas import (
    WorkTaskCreate,
    WorkTaskOut,
    WorkTaskUpdate,
    WorkTaskUpdateRate,
    WorkTaskUpdateStatus,
)

router = APIRouter(
    prefix=settings.prefix.work_tasks,
    tags=["Work Tasks"],
)


@router.post("", response_model=WorkTaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_input_schema: WorkTaskCreate,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    if not check_datetime_after_now(task_input_schema.complete_by):
        raise TaskBeforeNow

    task_adapter = WorkTaskAdapter(session)
    role_adapter = RoleAdapter(session)
    user_adapter = ModelAdapter(User, session)
    relation_adapter = RelationAdapter(session)

    current_user_role = await role_adapter.read_item_by_id(current_user.role_id)

    if not current_user_role:
        raise RoleNotFoundForUser

    assignee_user = await user_adapter.read_item_by_id(task_input_schema.assignee_id)
    assignee_user_role = await role_adapter.read_item_by_id(assignee_user.role_id)

    if not assignee_user_role:
        raise RoleNotFoundForUser

    relation = await relation_adapter.get_relation_by_superior_id_and_suboridinate_id(
        superior_id=current_user_role.id,
        subordinate_id=assignee_user_role.id,
    )

    if not relation:
        raise TaskForThisUser

    return await task_adapter.create_task_and_bound_user(
        task_input_schema, current_user.id
    )


@router.put("/{task_id}", response_model=WorkTaskOut)
async def update_task(
    task_id: int,
    task_input_schema: WorkTaskUpdate,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    if not check_datetime_after_now(task_input_schema.complete_by):
        raise TaskBeforeNow

    task_adapter = WorkTaskAdapter(session)

    task = await task_adapter.read_item_by_id(task_id)

    if not task:
        raise TasksNotFound

    if current_user.id != task.creator_id:
        raise NotTaskCreator

    return await task_adapter.update_item(task_input_schema, task)


@router.patch("/{task_id}/status", response_model=WorkTaskOut)
async def update_task_status(
    task_id: int,
    task_input_schema: WorkTaskUpdateStatus,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    task_adapter = WorkTaskAdapter(session)

    task = await task_adapter.read_item_by_id(task_id)

    if not task:
        raise TasksNotFound

    if current_user.id != task.assignee_id:
        raise NotTaskAssignee

    return await task_adapter.update_status(task_input_schema, task)


@router.patch("/{task_id}/rate", response_model=WorkTaskOut)
async def update_task_rate(
    task_id: int,
    task_input_schema: WorkTaskUpdateRate,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    task_adapter = WorkTaskAdapter(session)

    task = await task_adapter.read_item_by_id(task_id)

    if not task:
        raise TasksNotFound

    if current_user.id != task.creator_id:
        raise NotTaskCreator

    return await task_adapter.update_item(task_input_schema, task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    task_adapter = WorkTaskAdapter(session)

    task = await task_adapter.read_item_by_id(task_id)

    if not task:
        raise TasksNotFound

    if current_user.id != task.creator_id:
        raise NotTaskCreator

    await task_adapter.delete_item(task)


@router.get("/rating/me")
async def get_my_rating(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    task_adapter = WorkTaskAdapter(session)

    rating = await task_adapter.get_user_rating(assignee_id=current_user.id, days=90)

    if rating is None:
        raise TasksNotFound

    return {"rating": rating}


@router.get("/rating/team")
async def get_team_rating(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    task_adapter = WorkTaskAdapter(session)
    role_adapter = RoleAdapter(session)

    current_user_role = await role_adapter.read_item_by_id(current_user.role_id)

    if not current_user_role:
        raise RoleNotFoundForUser

    rating = await task_adapter.get_team_rating(current_user_role.structure_id, days=90)

    if rating is None:
        raise TasksNotFound

    return {"rating": rating}
