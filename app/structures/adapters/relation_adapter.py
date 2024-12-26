from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from structures.models import Relation
from structures.schemas.realtion import RelationCreate

from .model_adapter import ModelAdapter

RNM = TypeVar("RNM", bound=Relation)


class RelationAdapter(ModelAdapter):
    """Adapter class for performing database operations to the Relation model."""

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the adapter

        Args:
            session (AsyncSession): Async session
        """

        super().__init__(Relation, session)

    async def create_realtion_with_users_structure_id(
        self,
        relation_create_schema: RelationCreate,
        structure_id: int,
    ) -> RNM:
        """Creates new realtion and bounds it to structure.

        Args:
            relation_create_schema (RelationCreate): Pydantic schema to create relation
            structure_id (int): Structure id to bound

        Returns:
            RNM: Created relation object
        """
        relation = self.model(
            **relation_create_schema.model_dump(), structure_id=structure_id
        )

        self.session.add(relation)
        await self.session.commit()

        return relation
