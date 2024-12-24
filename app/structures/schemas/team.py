from pydantic import BaseModel


class TeamBase(BaseModel):
    name: str
    info: str

    model_config = {"from_attributes": True}


class TeamOut(TeamBase):
    id: int


class TeamCreate(TeamBase):
    structure_id: int
