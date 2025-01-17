import datetime

from sqlalchemy import DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.expression import text

from core.config import settings


class Base(DeclarativeBase):
    """Base abstract class for for SQLAlchemy ORM models.

    Attributes:
        id (int): Primary key
        created_at (datetime): Timestamp indicating when the record was created
        updated_at (datetime): Timestamp indicating when the record was last updated
    """

    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.main_db.naming_convention,
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), onupdate=text("now()")
    )
