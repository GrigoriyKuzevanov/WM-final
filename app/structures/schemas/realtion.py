from pydantic import BaseModel


class RelationBase(BaseModel):
    superior_id: int
    subordinate_id: int

    model_config = {"from_attributes": True}


class RelationOut(RelationBase):
    id: int
    structure_id: int


class RelationCreate(RelationBase):
    pass
