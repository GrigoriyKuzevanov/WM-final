from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from core.model_adapter import ModelAdapter
from work_tasks.models import WorkTask
from work_tasks.schemas import WorkTaskCreate, WorkTaskStatusEnum, WorkTaskUpdateStatus

WTM = TypeVar("WTM", bound=WorkTask)


class WorkTaskAdapter(ModelAdapter):
    """Adapter class for performing database operations to the WorkTask model."""

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the adapter

        Args:
            session (AsyncSession): Async session
        """

        super().__init__(WorkTask, session)

    async def create_task_and_bound_user(
        self,
        task_create_schema: WorkTaskCreate,
        creator_id: int,
    ) -> WTM:
        """Creates task with provided creator id.

        Args:
            task_create_schema (WorkTaskCreate): Pydantic schema to create task
            creator_id (int): Creator id

        Returns:
            WTM: Created WorkTask object
        """

        work_task = WorkTask(
            **task_create_schema.model_dump(),
            creator_id=creator_id,
            status=WorkTaskStatusEnum.CREATED.value,
            rate=0,
        )

        self.session.add(work_task)
        await self.session.commit()
        await self.session.refresh(work_task)

        return work_task

    async def update_status(
        self, status_update_schema: WorkTaskUpdateStatus, task: WorkTask
    ) -> WTM:
        """Updates status of the work task using WorkTaskStatusEnum values.

        Args:
            status_update_schema (WorkTaskUpdateStatus): Pydantic schema with data to
            update
            task (WorkTask): WorkTask object

        Returns:
            WTM: WorkTask object
        """

        new_status: WorkTaskStatusEnum = status_update_schema.model_dump().get("status")
        task.status = new_status.value

        await self.session.commit()
        await self.session.refresh(task)

        return task
