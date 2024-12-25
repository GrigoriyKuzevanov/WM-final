from typing import Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base

BM = TypeVar("BM", bound=Base)
PBM = TypeVar("PBM", bound=BaseModel)


class ModelAdapter:
    """Adapter class for performing database operations on SQLAlchemy models."""

    def __init__(self, model: Type[BM], session: AsyncSession) -> None:
        """Initializes the adapter

        Args:
            model (Type[BM]): SQLAlchemy model class
            session (AsyncSession): Async session
        """
        self.model = model
        self.session = session

    async def read_all_items(self) -> list[BM]:
        """Retrieves all items from db.

        Returns:
            list[BM]: List of all objects from db
        """

        stmt = select(self.model)
        results = await self.session.scalars(stmt)

        return results.all()

    async def read_item_by_id(self, item_id: int) -> BM | None:
        """Retrieves a single item by it's id

        Args:
            item_id (int): id of the item to retrieve

        Returns:
            BM | None: Object from the db or None if not found
        """

        result = await self.session.get(self.model, item_id)

        return result

    async def create_item(self, item_schema: PBM) -> BM:
        """Creates a new item using the provided schema.

        Args:
            item_schema (PBM): Pydantic schema containing item data

        Returns:
            BM: Created object from db
        """

        item = self.model(**item_schema.model_dump())

        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)

        return item

    async def update_item(self, update_schema: PBM, item: BM) -> BM:
        """Updates item with the provided schema.

        Args:
            update_schema (PBM): Pydantic schema with data to update
            item (BM): Object to update

        Returns:
            BM: Updated object from db
        """

        for key, value in update_schema.model_dump().items():
            setattr(item, key, value)

        await self.session.commit()
        await self.session.refresh(item)

        return item

    async def delete_item(self, item: BM) -> None:
        """Deletes item from db.

        Args:
            item (BM): Object to delete
        """

        await self.session.delete(item)
        await self.session.commit()
