from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.model_adapter import ModelAdapter
from structures.models import Relation
from structures.schemas.realtion import RelationCreate

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
        await self.session.refresh(relation)

        return relation

    async def get_relation_by_superior_id_and_suboridinate_id(
        self,
        superior_id: int,
        subordinate_id: int,
    ) -> RNM:
        """Gets relation with provided superior and subordinate ids."""

        stmt = select(Relation).where(
            Relation.superior_id == superior_id,
            Relation.subordinate_id == subordinate_id,
        )

        return await self.session.scalar(stmt)
