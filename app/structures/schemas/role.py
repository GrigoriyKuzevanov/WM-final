from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    info: str = Field(..., example="Sales manager middle")

    model_config = {"from_attributes": True}


class RoleOut(RoleBase):
    id: int
    name: str = Field(..., example="Manager")
    structure_id: int


class RoleUpdate(RoleBase):
    pass


class RoleCreate(RoleBase):
    name: str


class RoleCreateWithStructure(RoleCreate):
    structure_id: int
