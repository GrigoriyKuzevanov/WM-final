from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.model_adapter import ModelAdapter
from core.models import db_connector
from structures.adapters.relation_adapter import RelationAdapter
from structures.adapters.role_adapter import RoleAdapter
from users.dependencies.fastapi_users_routes import current_user
from users.models import User
from users.schemas import UserRead
from utils.check_time import check_datetime_after_now

from .adapters.work_task_adapter import WorkTaskAdapter
from .schemas import WorkTaskCreate, WorkTaskOut, WorkTaskUpdate

router = APIRouter(
    prefix=settings.prefix.work_tasks,
    tags=["Meetings"],
)


@router.post("", response_model=WorkTaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_input_schema: WorkTaskCreate,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    if not check_datetime_after_now(task_input_schema.complete_by):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't create meeting with datetime before now",
        )

    task_adapter = WorkTaskAdapter(session)
    role_adapter = RoleAdapter(session)
    user_adapter = ModelAdapter(User, session)
    relation_adapter = RelationAdapter(session)

    current_user_role = await role_adapter.read_item_by_id(current_user.role_id)

    if not current_user_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found role for this user"
        )

    assignee_user = await user_adapter.read_item_by_id(task_input_schema.assignee_id)
    assignee_user_role = await role_adapter.read_item_by_id(assignee_user.role_id)

    if not assignee_user_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )

    relation = await relation_adapter.get_relation_by_superior_id_and_suboridinate_id(
        superior_id=current_user_role.id,
        subordinate_id=assignee_user_role.id,
    )

    if not relation:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't create task for this user",
        )

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
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't update meeting with datetime before now",
        )

    task_adapter = WorkTaskAdapter(session)

    task = await task_adapter.read_item_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    if current_user.id != task.creator_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can't do this action"
        )

    return await task_adapter.update_item(task_input_schema, task)
