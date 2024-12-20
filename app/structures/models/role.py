from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base_model import Base

if TYPE_CHECKING:
    from users.models import User


association_table = Table(
    "roles_users_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE")),
)


class Role(Base):
    """A class for represtation roles table in the database"""

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(nullable=False)
    users: Mapped[list["User"]] = relationship(
        secondary=association_table, back_populates="roles", cascade="all, delete"
    )
