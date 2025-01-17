from pydantic import BaseModel, Field


class StructureBase(BaseModel):
    name: str = Field(..., example="Audit department")
    info: str = Field(..., example="Simple functional structure")

    model_config = {"from_attributes": True}


class StructureOut(StructureBase):
    id: int


class StructureUpdate(StructureBase):
    pass


class StructureCreate(StructureBase):
    pass
