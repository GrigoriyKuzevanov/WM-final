from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"

    @classmethod
    def get_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, cls)
