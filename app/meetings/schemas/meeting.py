from datetime import datetime

from pydantic import BaseModel

from users.schemas import UserRead


class MeetingBase(BaseModel):
    topic: str
    info: str
    meet_datetime: datetime

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
