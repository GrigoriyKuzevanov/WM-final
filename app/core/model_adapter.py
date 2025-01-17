from pydantic import BaseModel as PydanticSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base as SQLAlchemyBaseModel


class ModelAdapter:
    """Adapter class for performing database operations on SQLAlchemy models."""

    def __init__(self, model: SQLAlchemyBaseModel, session: AsyncSession) -> None:
        """Initializes the adapter

        Args:
            model (SQLAlchemyBaseModel): SQLAlchemy model class
            session (AsyncSession): Async session
        """
        self.model = model
        self.session = session

    async def read_all_items(self) -> list[SQLAlchemyBaseModel]:
        """Retrieves all items from db.

        Returns:
            list[SQLAlchemyBaseModel]: List of all objects from db
        """

        stmt = select(self.model)
        results = await self.session.scalars(stmt)

        return results.all()

    async def read_item_by_id(self, item_id: int) -> SQLAlchemyBaseModel | None:
        """Retrieves a single item by it's id

        Args:
            item_id (int): id of the item to retrieve

        Returns:
            SQLAlchemyBaseModel | None: Object from the db or None if not found
        """

        result = await self.session.get(self.model, item_id)

        return result

    async def create_item(self, item_schema: PydanticSchema) -> SQLAlchemyBaseModel:
        """Creates a new item using the provided schema.

        Args:
            item_schema (PydanticSchema): Pydantic schema containing item data

        Returns:
            SQLAlchemyBaseModel: Created object from db
        """

        item = self.model(**item_schema.model_dump())

        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)

        return item

    async def update_item(
        self, update_schema: PydanticSchema, item: SQLAlchemyBaseModel
    ) -> SQLAlchemyBaseModel:
        """Updates item with the provided schema.

        Args:
            update_schema (PydanticSchema): Pydantic schema with data to update
            item (SQLAlchemyBaseModel): Object to update

        Returns:
            SQLAlchemyBaseModel: Updated object from db
        """

        for key, value in update_schema.model_dump().items():
            setattr(item, key, value)

        await self.session.commit()
        await self.session.refresh(item)

        return item

    async def delete_item(self, item: SQLAlchemyBaseModel) -> None:
        """Deletes item from db.

        Args:
            item (SQLAlchemyBaseModel): Object to delete
        """

        await self.session.delete(item)
        await self.session.commit()
