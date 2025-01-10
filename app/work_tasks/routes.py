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


@router.post(
    "",
    response_model=WorkTaskOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new work task",
    description="""
    Creates a new work task using the provided schema. Requires authorization, the
    authenticated user registers as the work task's creator.

    Requirements:
    - The creator must have a role
    - The assignee user must exist
    - The assignee user must be a subordinate of the creator
    - The "complete_by" datetime for the work task must be in the future
    """,
)
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


@router.put(
    "/{task_id}",
    response_model=WorkTaskOut,
    summary="Update a work task",
    description="""
    Updates an existing work task. Requires authorization.

    Parameters:
    - task_id: The id of the work task to update

    Requirements:
    - A work task with provided id must exist
    - The current user must be creator of the work task
    - The "complete_by" datetime for the work task must be in the future
    """,
)
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


@router.patch(
    "/{task_id}/status",
    response_model=WorkTaskOut,
    summary="Update a work task's status",
    description="""
    Updates status of the work task with provided id. Requires authorization.

    Parameters:
    - task_id: The id of the work task to update

    Requirements:
    - A work task with provided id must exist
    - The current user must be assignee of the work task
    """,
)
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


@router.patch(
    "/{task_id}/rate",
    response_model=WorkTaskOut,
    summary="Update a work task's rate",
    description="""
    Updates a rate of the work task with provided id. Requires authorization.

    Parameters:
    - task_id: The id of the work task to update

    Requirements:
    - A work task with provided id must exist
    - The current user must be creator of the work task
    """,
)
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


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a work task",
    description="""
    Deletes a work task with provided id. Requires authorization.

    Parameters:
    - task_id: The id of the work task to delete

    Requirements:
    - A work task with provided id must exist
    - The current user must be creator of the work task
    """,
)
async def delete_task(
    task_id: int,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    tasks_adapter = WorkTaskAdapter(session)

    tasks_service = WorkTaskService(tasks_adapter)

    await tasks_service.delete_task(task_id=task_id, user_id=current_user.id)


@router.get(
    "/rating/me",
    summary="Get user's work tasks rating",
    description="""
    Retrieves an average rate of the completed work tasks of the current user. Requires
    authorization.

    Requirements:
    - The current user must have at least one completed work task for past 90 days.
    """,
)
async def get_my_rating(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    tasks_adapter = WorkTaskAdapter(session)

    tasks_service = WorkTaskService(tasks_adapter)

    return await tasks_service.get_user_rating(user_id=current_user.id)


@router.get(
    "/rating/team",
    summary="Get team's work tasks rating",
    description="""
    Retrieves an average rate of the completed work tasks of the current user's team.
    Requires authorization.

    Requirements:
    - The current user must have an associated role (be a member of existing structure)
    - The team members must have at least one completed work task for past 90 days.
    """,
)
async def get_team_rating(
    current_user_role: RoleOut = Depends(current_user_role),
    session: AsyncSession = Depends(db_connector.get_session),
):
    tasks_adapter = WorkTaskAdapter(session)

    tasks_service = WorkTaskService(tasks_adapter)

    return await tasks_service.get_team_rating(
        structure_id=current_user_role.structure_id
    )


@router.get(
    "/me-assigned",
    response_model=list[WorkTaskOut],
    summary="Get the user assigned work tasks",
    description="""
    Retrieves all the work tasks which have the current user as an assignee. Requires
    authorization.
    """,
)
async def get_my_assigned_tasks(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    tasks_adapter = WorkTaskAdapter(session)

    tasks_service = WorkTaskService(tasks_adapter)

    return await tasks_service.get_user_assigned_tasks(current_user.id)


@router.get(
    "/me-created",
    response_model=list[WorkTaskOut],
    summary="Get the user created work tasks",
    description="""
    Retrieves all the work tasks which have the current user as a creator. Requires
    authorization.
    """,
)
async def get_my_created_tasks(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    tasks_adapter = WorkTaskAdapter(session)

    tasks_service = WorkTaskService(tasks_adapter)

    return await tasks_service.get_user_created_tasks(current_user.id)
