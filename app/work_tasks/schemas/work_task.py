from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class WorkTaskStatusEnum(Enum):
    CREATED = "CREATED"
    IN_WORK = "IN_WORK"
    COMPLETED = "COMPLETED"


class WorkTaskBase(BaseModel):
    name: str
    description: str
    comments: str
    complete_by: datetime

    model_config = {"from_attributes": True}


class WorkTaskCreate(WorkTaskBase):
    assignee_id: int


class WorkTaskOut(WorkTaskBase):
    id: int
    rate: int
    status: str
    creator_id: int
    assignee_id: int


class WorkTaskUpdate(WorkTaskBase):
    pass


class WorkTaskUpdateStatus(BaseModel):
    status: WorkTaskStatusEnum


class WorkTaskUpdateRate(BaseModel):
    rate: int = Field(..., gt=0, le=5)
