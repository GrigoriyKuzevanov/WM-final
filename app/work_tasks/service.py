from core.model_adapter import ModelAdapter
from structures.adapters.relation_adapter import RelationAdapter
from structures.adapters.role_adapter import RoleAdapter
from structures.exceptions.role import RoleNotFound
from users.exceptions import UserNotFound
from utils.check_time import check_datetime_after_now

from .adapters.work_task_adapter import WorkTaskAdapter
from .exceptions import (
    NotTaskAssignee,
    NotTaskCreator,
    TaskBeforeNow,
    TaskForThisUser,
    TasksNotFound,
)
from .models import WorkTask
from .schemas import (
    WorkTaskCreate,
    WorkTaskUpdate,
    WorkTaskUpdateRate,
    WorkTaskUpdateStatus,
)


class WorkTaskService:
    """Work tasks managing service."""

    def __init__(self, tasks_adapter: WorkTaskAdapter) -> None:
        """Inits WorkTaskService.

        Args:
            tasks_adapter (WorkTaskAdapter): Adapter to interacting with database
        """

        self.tasks_adapter = tasks_adapter

    async def create_task(
        self,
        user_id: int,
        user_role_id: int,
        task_create_schema: WorkTaskCreate,
        users_adapter: ModelAdapter,
        roles_adapter: RoleAdapter,
        relations_adapter: RelationAdapter,
    ) -> WorkTask:
        """Creates a new work task.

        Args:
            user_id (int): User id
            user_role_id (int): User role id
            task_create_schema (WorkTaskCreate): Schema to create work task
            users_adapter (ModelAdapter): Users adapter
            roles_adapter (RoleAdapter): Roles adapter
            relations_adapter (RelationAdapter): Relations adapter

        Raises:
            TaskBeforeNow: If work task complete by datetime is before now
            UserNotFound: If user with provided id not found
            RoleNotFound: If role with provided id not found
            TaskForThisUser: If user with provided id is not superior for creating work
            task's assignee user

        Returns:
            WorkTask: Created work task model
        """

        if not check_datetime_after_now(task_create_schema.complete_by):
            raise TaskBeforeNow

        assignee_user = await users_adapter.read_item_by_id(
            task_create_schema.assignee_id
        )

        if not assignee_user:
            raise UserNotFound

        assignee_user_role = await roles_adapter.read_item_by_id(assignee_user.role_id)

        if not assignee_user_role:
            raise RoleNotFound

        relation = (
            await relations_adapter.get_relation_by_superior_id_and_suboridinate_id(
                superior_id=user_role_id,
                subordinate_id=assignee_user_role.id,
            )
        )

        if not relation:
            raise TaskForThisUser

        return await self.tasks_adapter.create_task_and_bound_user(
            task_create_schema, user_id
        )

    async def get_task_by_creator(self, task_id: int, creator_id: int) -> WorkTask:
        """Get work task by creator

        Args:
            task_id (int): Work task id
            creator_id (int): Creator id

        Raises:
            TasksNotFound: If work task with provided id not found
            NotTaskCreator: If creator id is not creator_id of found task

        Returns:
            WorkTask: Work task model
        """

        task = await self.tasks_adapter.read_item_by_id(task_id)

        if not task:
            raise TasksNotFound

        if not creator_id == task.creator_id:
            raise NotTaskCreator

        return task

    async def update_task(
        self, task_id: int, user_id: int, task_update_schema: WorkTaskUpdate
    ) -> WorkTask:
        """Updates work task.

        Args:
            task_id (int): Work task id
            user_id (int): User id
            task_update_schema (WorkTaskUpdate): Schema to update work task

        Raises:
            TaskBeforeNow: If complete_by datetime to update is before now

        Returns:
            WorkTask: Updated work task model
        """

        if not check_datetime_after_now(task_update_schema.complete_by):
            raise TaskBeforeNow

        task = await self.get_task_by_creator(task_id=task_id, creator_id=user_id)

        return await self.tasks_adapter.update_item(task_update_schema, task)

    async def update_task_status(
        self, task_id: int, user_id: int, task_update_schema: WorkTaskUpdateStatus
    ) -> WorkTask:
        """Updates work task status.

        Args:
            task_id (int): Work task id
            user_id (int): User id
            task_update_schema (WorkTaskUpdate): Schema to update work task

        Raises:
            TasksNotFound: If work task status with provided id not found
            NotTaskAssignee: If user with provided id is not assignee of the work task

        Returns:
            WorkTask: Updated work task model
        """

        task = await self.tasks_adapter.read_item_by_id(task_id)

        if not task:
            raise TasksNotFound

        if not user_id == task.assignee_id:
            raise NotTaskAssignee

        return await self.tasks_adapter.update_status(task_update_schema, task)

    async def update_task_rate(
        self, task_id: int, user_id: int, task_update_schema: WorkTaskUpdateRate
    ) -> WorkTask:
        """Updates work task rate.

        Args:
            task_id (int): Work task id
            user_id (int): User id
            task_update_schema (WorkTaskUpdate): Schema to update work task

        Returns:
            WorkTask: Updated work task model
        """
        task = await self.get_task_by_creator(task_id=task_id, creator_id=user_id)

        return await self.tasks_adapter.update_item(task_update_schema, task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        """Deletes work task.

        Args:
            task_id (int): Work task id
            user_id (int): User id
        """

        task = await self.get_task_by_creator(task_id=task_id, creator_id=user_id)

        await self.tasks_adapter.delete_item(task)

    async def get_user_rating(self, user_id: int) -> dict:
        """Get user's work tasks average rating for 90 days.

        Args:
            user_id (int): User id

        Raises:
            TasksNotFound: If user doesn't have rating work tasks in 90 days

        Returns:
            dict: Dict {"rating": <user's average rating>}
        """

        rating = await self.tasks_adapter.get_user_rating(assignee_id=user_id, days=90)

        if rating is None:
            raise TasksNotFound

        return {"rating": rating}

    async def get_team_rating(self, structure_id: int) -> dict:
        """Get team average rating for 90 days.

        Args:
            structure_id (int): Structure id

        Raises:
            TasksNotFound: If team doesn't have rating work tasks in 90 days

        Returns:
            dict: Dict {"rating": <team's average rating>}
        """

        rating = await self.tasks_adapter.get_team_rating(
            structure_id=structure_id, days=90
        )

        if rating is None:
            raise TasksNotFound

        return {"rating": rating}
