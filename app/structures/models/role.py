from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request

from core.models.base_model import Base
from structures.models.structure import (
    association_table as roles_structures_association,
)

if TYPE_CHECKING:
    from structures.models import Relation, Structure
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
    structures: Mapped[list["Structure"]] = relationship(
        secondary=roles_structures_association,
        back_populates="roles",
        cascade="all, delete",
    )
    superiors: Mapped[list["Relation"]] = relationship(
        foreign_keys="Relation.superior_id", back_populates="superior"
    )
    subordinates: Mapped[list["Relation"]] = relationship(
        foreign_keys="Relation.subordinate_id", back_populates="subordinate"
    )

    async def __admin_repr__(self, request: Request) -> str:
        """Model's representation in admin.

        Args:
            request (_type_): Request instance

        Returns:
            str: Model's string representation
        """

        return f"{self.name}"
