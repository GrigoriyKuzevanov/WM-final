import decimal
from typing import TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.model_adapter import ModelAdapter
from structures.models import Role
from users.models import User
from utils.get_date_days_ago import get_date_days_ago
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

    async def get_user_rating(
        self, assignee_id: int, days: int
    ) -> decimal.Decimal | None:
        """Gets average user's task rate for provided number of days.

        Args:
            assignee_id (int): Assignee id for filter
            days (int): Number of days

        Returns:
            decimal.Decimal | None: Average rating or None if no rates
        """

        stmt = select(func.avg(self.model.rate)).where(
            self.model.assignee_id == assignee_id,
            self.model.status == WorkTaskStatusEnum.COMPLETED.value,
            self.model.complete_by >= get_date_days_ago(days=days),
        )

        return await self.session.scalar(stmt)

    async def get_team_rating(
        self, structure_id: int, days: int
    ) -> decimal.Decimal | None:
        """Gets average team's task rate for provided number of days.

        Args:
            structure_id (int): Structre id for filter
            days (int): Number of days

        Returns:
            decimal.Decimal | None: Average rating or None if no rates
        """

        stmt = (
            select(func.avg(self.model.rate))
            .join(User, self.model.assignee_id == User.id)
            .join(Role, User.role_id == Role.id)
            .where(
                Role.structure_id == structure_id,
                self.model.complete_by >= get_date_days_ago(days=days),
            )
        )

        return await self.session.scalar(stmt)
