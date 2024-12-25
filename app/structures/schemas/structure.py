from pydantic import BaseModel


class StructureBase(BaseModel):
    name: str
    info: str

    model_config = {"from_attributes": True}


class StructureOut(StructureBase):
    id: int


class StructureUpdate(StructureBase):
    pass


class StructureCreate(StructureBase):
    pass
