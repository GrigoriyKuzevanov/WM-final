from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.model_adapter import ModelAdapter
from core.models import User, db_connector
from structures.adapters.role_adapter import RoleAdapter
from structures.exceptions.role import RoleNotFoundForUser
from users.dependencies.fastapi_users_routes import current_user
from users.exceptions import UserNotFound
from users.schemas import UserRead
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
from .schemas.meeting import MeetingCreate, MeetingOut, MeetingOutUsers, MeetingUpdate

router = APIRouter(
    prefix=settings.prefix.meetings,
    tags=["Meetings"],
)


@router.post("", response_model=MeetingOut, status_code=status.HTTP_201_CREATED)
async def create_meeting(
    meeting_input_schema: MeetingCreate,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    if not check_datetime_after_now(meeting_input_schema.meet_datetime):
        raise MeetingBeforeNow

    meeting_adapter = MeetingAdapter(session)
    role_adapter = RoleAdapter(session)

    current_user_role = await role_adapter.read_item_by_id(current_user.role_id)

    if not current_user_role:
        raise RoleNotFoundForUser

    return await meeting_adapter.create_meeting_by_user(
        current_user.id, meeting_input_schema
    )


@router.put("/{meeting_id}", response_model=MeetingOut)
async def update_meeting(
    meeting_id: int,
    meeting_input_schema: MeetingUpdate,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    if not check_datetime_after_now(meeting_input_schema.meet_datetime):
        raise MeetingBeforeNow

    meeting_adapter = MeetingAdapter(session)
    meeting = await meeting_adapter.read_item_by_id(meeting_id)

    if not meeting:
        raise MeetingsNotFound

    if not meeting.creator_id == current_user.id:
        raise NotMeetingCreator

    return await meeting_adapter.update_item(meeting_input_schema, meeting)


@router.delete("/{meeting_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meeting(
    meeting_id: int,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    meeting_adapter = MeetingAdapter(session)
    meeting = await meeting_adapter.read_item_by_id(meeting_id)

    if not meeting:
        raise MeetingsNotFound

    if not meeting.creator_id == current_user.id:
        raise NotMeetingCreator

    await meeting_adapter.delete_item(meeting)


@router.get("/{meeting_id}/add-user/{user_id}", response_model=MeetingOutUsers)
async def add_user(
    meeting_id: int,
    user_id: int,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    meeting_adapter = MeetingAdapter(session)
    user_adapter = ModelAdapter(User, session)
    meeting = await meeting_adapter.get_meeting_with_users(meeting_id)

    if not meeting:
        raise MeetingsNotFound

    if not meeting.creator_id == current_user.id:
        raise NotMeetingCreator

    user = await user_adapter.read_item_by_id(user_id)

    if not user:
        raise UserNotFound

    if user in meeting.users:
        raise UserAlreadyAdded

    return await meeting_adapter.add_user(meeting, user)


@router.get("/{meeting_id}/remove-user/{user_id}", response_model=MeetingOutUsers)
async def remove_user(
    meeting_id: int,
    user_id: int,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    meeting_adapter = MeetingAdapter(session)
    user_adapter = ModelAdapter(User, session)
    meeting = await meeting_adapter.get_meeting_with_users(meeting_id)

    if not meeting:
        raise MeetingsNotFound

    if not meeting.creator_id == current_user.id:
        raise NotMeetingCreator

    user = await user_adapter.read_item_by_id(user_id)

    if not user:
        raise UserNotFound

    if user not in meeting.users:
        raise UserNotFoundInMeeting

    return await meeting_adapter.remove_user(meeting, user)


@router.get("/my", response_model=list[MeetingOut])
async def get_my_meetings(
    today: bool = False,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    meeting_adapter = MeetingAdapter(session)
    meetings = await meeting_adapter.read_by_user_id(current_user.id)

    if today:
        meetings = [
            meeting
            for meeting in meetings
            if check_date_is_today(meeting.meet_datetime)
        ]
    else:
        meetings = [
            meeting for meeting in meetings if check_after_now(meeting.meet_datetime)
        ]

    return meetings
