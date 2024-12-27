from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.model_adapter import ModelAdapter
from core.models import User, db_connector
from structures.adapters.role_adapter import RoleAdapter
from users.dependencies.fastapi_users_routes import current_user
from users.schemas import UserRead
from utils.check_time import check_datetime_after_now

from .adapters.meeting_adapter import MeetingAdapter
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
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't create meeting with datetime before now",
        )

    meeting_adapter = MeetingAdapter(session)
    role_adapter = RoleAdapter(session)

    current_user_role = await role_adapter.read_item_by_id(current_user.role_id)

    if not current_user_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found role for this user"
        )

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
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't create meeting with datetime before now",
        )

    meeting_adapter = MeetingAdapter(session)
    meeting = await meeting_adapter.read_item_by_id(meeting_id)

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found"
        )

    if not meeting.creator_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="YYou can't do this action",
        )

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found"
        )

    if not meeting.creator_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't do this action",
        )

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found"
        )

    if not meeting.creator_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't do this action",
        )

    user = await user_adapter.read_item_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user in meeting.users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User already added"
        )

    return await meeting_adapter.add_user(meeting, user)


@router.get("/{meeting_id}/remove-user/{user_id}", response_model=MeetingOutUsers)
async def reomve_user(
    meeting_id: int,
    user_id: int,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    meeting_adapter = MeetingAdapter(session)
    user_adapter = ModelAdapter(User, session)
    meeting = await meeting_adapter.get_meeting_with_users(meeting_id)

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found"
        )

    if not meeting.creator_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't do this action",
        )

    user = await user_adapter.read_item_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user not in meeting.users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found in meeting users",
        )

    return await meeting_adapter.remove_user(meeting, user)


@router.get("/my", response_model=list[MeetingOut])
async def get_my_meetings(
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    meeting_adapter = MeetingAdapter(session)

    return await meeting_adapter.read_by_user_id(current_user.id)
