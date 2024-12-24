from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    info: str

    model_config = {"from_attributes": True}


class RoleOut(RoleBase):
    id: int
    structure_id: int


class RoleCreate(RoleBase):
    structure_id: int
