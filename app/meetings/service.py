from core.model_adapter import ModelAdapter
from users.exceptions import UserNotFound
from utils.check_after_now import check_after_now
from utils.check_time import check_datetime_after_now
from utils.check_today import check_date_is_today

from .adapters.meeting_adapter import MeetingAdapter
from .exceptions import (
    MeetingBeforeNow,
    MeetingsNotFound,
    NotMeetingCreator,
    UserAlreadyAdded,
    UserNotFoundInMeeting,
)
from .models import Meeting
from .schemas.meeting import MeetingCreate, MeetingUpdate


class MeetingService:
    """Meetings managing service."""

    def __init__(self, meetings_adapter: MeetingAdapter) -> None:
        """Inits MeetingService.

        Args:
            meetings_adapter (MeetingAdapter): Adapter to interacting with database
        """

        self.meetings_adapter = meetings_adapter

    async def get_meeting_by_creator(self, meeting_id: int, user_id: int) -> Meeting:
        """Get meeting by creator.

        Args:
            meeting_id (int): Meeting id to get
            user_id (int): Creator id

        Raises:
            MeetingsNotFound: If meeting with provided id not found
            NotMeetingCreator: If user is not creator of meeting

        Returns:
            Meeting: Meeting model
        """

        meeting = await self.meetings_adapter.read_item_by_id(meeting_id)

        if not meeting:
            raise MeetingsNotFound

        if not meeting.creator_id == user_id:
            raise NotMeetingCreator

        return meeting

    async def get_meeting_with_users_by_creator(
        self, meeting_id: int, user_id: int
    ) -> Meeting:
        """Get meeting with loaded users by creator.

        Args:
            meeting_id (int): Meeting id to get
            user_id (int): Creator id

        Raises:
            MeetingsNotFound: If meeting with provided id not found
            NotMeetingCreator: If user is not creator of meeting

        Returns:
            Meeting: Meeting model with loaded users
        """

        meeting = await self.meetings_adapter.get_meeting_with_users(meeting_id)

        if not meeting:
            raise MeetingsNotFound

        if not meeting.creator_id == user_id:
            raise NotMeetingCreator

        return meeting

    async def create_meeting(
        self, creator_id: int, meeting_create_schema: MeetingCreate
    ) -> Meeting:
        """Creates a mew meeting.

        Args:
            creator_id (int): Creator id
            meeting_create_schema (MeetingCreate): Schema to create a meeting

        Raises:
            MeetingBeforeNow: If meeting meet datetime is before now

        Returns:
            Meeting: Created meeting model
        """

        if not check_datetime_after_now(meeting_create_schema.meet_datetime):
            raise MeetingBeforeNow

        return await self.meetings_adapter.create_meeting_by_user(
            creator_id, meeting_create_schema
        )

    async def update_meeting(
        self,
        meeting_id: int,
        user_id: int,
        meeting_update_schema: MeetingUpdate,
    ) -> Meeting:
        """Updates meeting by creator

        Args:
            meeting_id (int): Id of the meeting to update
            user_id (int): Id of the meeting creator
            meeting_update_schema (MeetingUpdate): Schema to update meeting

        Raises:
            MeetingBeforeNow: If meet_datetime to update is before now

        Returns:
            Meeting: Updated meeting model
        """

        if not check_datetime_after_now(meeting_update_schema.meet_datetime):
            raise MeetingBeforeNow

        meeting = await self.get_meeting_by_creator(meeting_id, user_id)

        return await self.meetings_adapter.update_item(meeting_update_schema, meeting)

    async def delete_meeting(self, meeting_id: int, user_id: int) -> None:
        """Deletes meeting by creator.

        Args:
            meeting_id (int): Id of the meeting to update
            user_id (int): Id of the meeting creator
        """

        meeting = await self.get_meeting_by_creator(meeting_id, user_id)

        await self.meetings_adapter.delete_item(meeting)

    async def add_user(
        self,
        meeting_id: int,
        user_to_add_id: int,
        creator_id: int,
        users_adapter: ModelAdapter,
    ) -> Meeting:
        """Add user to meeting users.

        Args:
            meeting_id (int): Meeting id
            user_to_add_id (int): Id of the user to add
            creator_id (int): Meeting creator id
            users_adapter (ModelAdapter): Adapter to interactive with database

        Raises:
            UserNotFound: If user not found
            UserAlreadyAdded: If user already added to meeting

        Returns:
            Meeting: Meeting model with added users
        """

        meeting = await self.get_meeting_with_users_by_creator(meeting_id, creator_id)

        user = await users_adapter.read_item_by_id(user_to_add_id)

        if not user:
            raise UserNotFound

        if user in meeting.users:
            raise UserAlreadyAdded

        return await self.meetings_adapter.add_user(meeting, user)

    async def remove_user(
        self,
        meeting_id: int,
        user_to_remove_id: int,
        creator_id: int,
        users_adapter: ModelAdapter,
    ) -> Meeting:
        """Remove user from meeting users.

        Args:
            meeting_id (int): Meeting id
            user_to_remove_id (int): Id of the user to remove
            creator_id (int): Meeting creator id
            users_adapter (ModelAdapter): Adapter to interactive with database

        Raises:
            UserNotFound: If user not found
            UserNotFoundInMeeting: If user is not in meeting users

        Returns:
            Meeting: Meeting model
        """

        meeting = await self.get_meeting_with_users_by_creator(meeting_id, creator_id)

        user = await users_adapter.read_item_by_id(user_to_remove_id)

        if not user:
            raise UserNotFound

        if user not in meeting.users:
            raise UserNotFoundInMeeting

        return await self.meetings_adapter.remove_user(meeting, user)

    async def get_user_meetings(self, user_id: int, today: bool) -> list[Meeting]:
        """Retrieve user meetings.

        Args:
            user_id (int): User id
            today (bool): True if need to get today only meetings, False if need to get
            all meetings

        Returns:
            list[Meeting]: List of meeting models
        """

        meetings = await self.meetings_adapter.read_by_user_id(user_id)

        if today:
            meetings = [
                meeting
                for meeting in meetings
                if check_date_is_today(meeting.meet_datetime)
            ]
        else:
            meetings = [
                meeting
                for meeting in meetings
                if check_after_now(meeting.meet_datetime)
            ]

        return meetings
