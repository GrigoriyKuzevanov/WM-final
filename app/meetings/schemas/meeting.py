from datetime import datetime

from pydantic import BaseModel, Field

from users.schemas import UserRead


class MeetingBase(BaseModel):
    topic: str = Field(..., example="Introduction")
    info: str = Field(..., example="Team introduction meeting")
    meet_datetime: datetime = Field(..., example="2025-02-10T08:30:00")

    model_config = {"from_attributes": True}


class MeetingOut(MeetingBase):
    id: int
    creator_id: int


class MeetingUpdate(MeetingBase):
    pass


class MeetingCreate(MeetingBase):
    pass


class MeetingOutUsers(MeetingOut):
    users: list[UserRead]
