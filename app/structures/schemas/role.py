from pydantic import BaseModel


class RoleBase(BaseModel):
    info: str

    model_config = {"from_attributes": True}


class RoleOut(RoleBase):
    id: int
    name: str
    structure_id: int


class RoleUpdate(RoleBase):
    pass


class RoleCreate(RoleBase):
    name: str
