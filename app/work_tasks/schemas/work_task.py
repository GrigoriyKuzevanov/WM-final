from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class WorkTaskStatusEnum(Enum):
    CREATED = "CREATED"
    IN_WORK = "IN_WORK"
    COMPLETED = "COMPLETED"


class WorkTaskBase(BaseModel):
    name: str = Field(..., example="Prepare report")
    description: str = Field(..., example="Prepare a very important work report")
    comments: str = Field(..., example="Report must include all the work details")
    complete_by: datetime = Field(..., example="2025-02-10T08:30:00")

    model_config = {"from_attributes": True}


class WorkTaskCreate(WorkTaskBase):
    assignee_id: int


class WorkTaskOut(WorkTaskBase):
    id: int
    rate: int = Field(..., ge=0, le=5)
    status: WorkTaskStatusEnum
    creator_id: int
    assignee_id: int


class WorkTaskUpdate(WorkTaskBase):
    pass


class WorkTaskUpdateStatus(BaseModel):
    status: WorkTaskStatusEnum


class WorkTaskUpdateRate(BaseModel):
    rate: int = Field(..., ge=0, le=5)
