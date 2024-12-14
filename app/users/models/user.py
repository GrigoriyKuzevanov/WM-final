from fastapi_users.db import SQLAlchemyBaseUserTable

from core.database import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"
