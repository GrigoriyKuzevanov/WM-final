from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request

from core.models.base_model import Base

if TYPE_CHECKING:
    from structures.models import Relation, Structure
    from users.models import User


class Role(Base):
    """A class for represtation roles table in the database."""

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(nullable=False)
    info: Mapped[str]
    structure_id: Mapped[int] = mapped_column(
        ForeignKey("structures.id", ondelete="CASCADE"), nullable=False
    )

    users: Mapped[list["User"]] = relationship(back_populates="role")
    structure: Mapped["Structure"] = relationship(
        back_populates="roles",
    )
    superiors: Mapped[list["Relation"]] = relationship(
        foreign_keys="Relation.superior_id",
        back_populates="superior",
        cascade="all, delete",
    )
    subordinates: Mapped[list["Relation"]] = relationship(
        foreign_keys="Relation.subordinate_id",
        back_populates="subordinate",
        cascade="all, delete",
    )

    async def __admin_repr__(self, request: Request) -> str:
        """Model's representation in admin.

        Args:
            request (_type_): Request instance

        Returns:
            str: Model's string representation
        """

        return f"{self.name}"
