from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.model_adapter import ModelAdapter
from core.models import User, db_connector
from structures.dependencies.role import current_user_role
from users.dependencies.fastapi_users_routes import current_user
from users.schemas import UserRead

from .adapters.meeting_adapter import MeetingAdapter
from .schemas.meeting import MeetingCreate, MeetingOut, MeetingOutUsers, MeetingUpdate
from .service import MeetingService

router = APIRouter(
    prefix=settings.prefix.meetings,
    tags=["Meetings"],
)


@router.post(
    "",
    response_model=MeetingOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_user_role)],
    summary="Create a new meeting",
    description="""
    Creates a new meeting using the provided schema. Requires authorization, the
    authenticated user registers as the meetings's creator.

    Requirements:
    - The "meet_datetime" datetime for the meeting must be in the future
    """,
)
async def create_meeting(
    meeting_input_schema: MeetingCreate,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    meetings_adapter = MeetingAdapter(session)

    meetings_service = MeetingService(meetings_adapter)

    return await meetings_service.create_meeting(
        creator_id=current_user.id,
        meeting_create_schema=meeting_input_schema,
    )


@router.put(
    "/{meeting_id}",
    response_model=MeetingOut,
    summary="Update a meeting",
    description="""
    Updates an existing meeting. Requires authorization.

    Parameters:
    - meeting_id: The id of the meeting to update

    Requirements:
    - A meeting with provided id must exist
    - The current user must be creator of the meeting
    - The "meet_datetime" datetime for the meeting must be in the future
    """,
)
async def update_meeting(
    meeting_id: int,
    meeting_input_schema: MeetingUpdate,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    meetings_adapter = MeetingAdapter(session)

    meetings_service = MeetingService(meetings_adapter)

    return await meetings_service.update_meeting(
        meeting_id=meeting_id,
        user_id=current_user.id,
        meeting_update_schema=meeting_input_schema,
    )


@router.delete(
    "/{meeting_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a meeting",
    description="""
    Deletes a meeting with provided id. Requires authorization.

    Parameters:
    - meeting_id: The id of the meeting to delete

    Requirements:
    - A meeting with provided id must exist
    - The current user must be creator of the meeting
    """,
)
async def delete_meeting(
    meeting_id: int,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    meetings_adapter = MeetingAdapter(session)

    meetings_service = MeetingService(meetings_adapter)

    await meetings_service.delete_meeting(meeting_id, current_user.id)


@router.get(
    "/{meeting_id}/add-user/{user_id}",
    response_model=MeetingOutUsers,
    summary="Add a user to a meeting",
    description="""
    Adds user with provided id to a meeting with provided id. Requires authorization.

    Parameters:
    - meeting_id: The id of the meeting to add the user to
    - user_id: The id of the user to add to the meeting

    Requirements:
    - The current user must be the creator of the meeting
    - A user with the provided id must exist
    - A user with the provided id must not already be in the meeting users
    """,
)
async def add_user(
    meeting_id: int,
    user_id: int,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    meetings_adapter = MeetingAdapter(session)
    users_adapter = ModelAdapter(User, session)

    meetings_service = MeetingService(meetings_adapter)

    return await meetings_service.add_user(
        meeting_id=meeting_id,
        user_to_add_id=user_id,
        creator_id=current_user.id,
        users_adapter=users_adapter,
    )


@router.get(
    "/{meeting_id}/remove-user/{user_id}",
    response_model=MeetingOutUsers,
    summary="Remove a user from a meeting users",
    description="""
    Removes user with provided id from a meeting with provided id. Requires
    authorization.

    Parameters:
    - meeting_id: The id of the meeting to remove the user from
    - user_id: The id of the user to remove from the meeting

    Requirements:
    - The current user must be the creator of the meeting
    - A user with the provided id must exist
    - A user with the provided id must be in the meeting users
    """,
)
async def remove_user(
    meeting_id: int,
    user_id: int,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    meetings_adapter = MeetingAdapter(session)
    users_adapter = ModelAdapter(User, session)

    meetings_service = MeetingService(meetings_adapter)

    return await meetings_service.remove_user(
        meeting_id=meeting_id,
        user_to_remove_id=user_id,
        creator_id=current_user.id,
        users_adapter=users_adapter,
    )


@router.get(
    "/my",
    response_model=list[MeetingOut],
    summary="Get user's meetings",
    description="""
    Retrieves all the user's meetings. Requires authorization.

    Parameters:
    - today: If true retrieves only today meetings, if false - all the user's meetings
    """,
)
async def get_my_meetings(
    today: bool = False,
    current_user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(db_connector.get_session),
):
    meetings_adapter = MeetingAdapter(session)

    meetings_service = MeetingService(meetings_adapter)

    return await meetings_service.get_user_meetings(
        user_id=current_user.id, today=today
    )
