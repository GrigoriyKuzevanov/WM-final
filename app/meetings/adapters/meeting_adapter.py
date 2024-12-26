from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.model_adapter import ModelAdapter
from meetings.models import Meeting
from meetings.schemas.meeting import MeetingCreate
from users.models import User

MM = TypeVar("MM", bound=Meeting)


class MeetingAdapter(ModelAdapter):
    """Adapter class for performing database operations to the Meeting model."""

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the adapter

        Args:
            session (AsyncSession): Async session
        """

        super().__init__(Meeting, session)

    async def get_meeting_with_users(self, meeting_id: int) -> MM:
        """Gets Meeting with provided id with joined loaded users.

        Args:
            meeting_id (int): Meeting id

        Returns:
            MM: Meeting object
        """

        stmt = (
            select(Meeting)
            .options(joinedload(Meeting.users))
            .where(Meeting.id == meeting_id)
        )

        return await self.session.scalar(stmt)

    async def create_meeting_by_user(
        self, current_user_id: int, meeting_schema: MeetingCreate
    ) -> MM:
        """Creates meeting with provided schema and current user as a creator.

        Args:
            current_user_id (int): Current user id
            meeting_schema (MeetingCreate): Meeting create schema

        Returns:
            MM: Created meeting object
        """

        meeting = Meeting(**meeting_schema.model_dump(), creator_id=current_user_id)

        self.session.add(meeting)
        await self.session.commit()
        await self.session.refresh(meeting)

        return meeting

    async def add_user(self, meeting: Meeting, user: User) -> MM:
        """Add user to meeting.

        Args:
            meeting (Meeting): Meeting object
            user (User): User object

        Returns:
            MM: Meeting object with added user
        """

        meeting.users.append(user)

        self.session.add(meeting)
        await self.session.commit()

        return meeting

    async def remove_user(self, meeting: Meeting, user: User) -> MM:
        """Remove user from meeting.

        Args:
            meeting (Meeting): Meeting object
            user (User): User object

        Returns:
            MM: Meeting object with removed user
        """

        meeting.users.remove(user)

        self.session.add(meeting)
        await self.session.commit()

        return meeting
