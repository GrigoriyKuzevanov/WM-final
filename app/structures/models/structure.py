from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request

from core.models.base_model import Base

if TYPE_CHECKING:
    from .relation import Relation
    from .role import Role
    from .team import Team


association_table = Table(
    "roles_structures_association",
    Base.metadata,
    Column("structure_id", ForeignKey("structures.id", ondelete="CASCADE")),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE")),
)


class Structure(Base):
    """A class for represtation structures table in the database"""

    __tablename__ = "structures"

    name: Mapped[str] = mapped_column(nullable=False)
    roles: Mapped[list["Role"]] = relationship(
        secondary=association_table,
        back_populates="structures",
        cascade="all, delete",
    )
    relations: Mapped[list["Relation"]] = relationship(back_populates="structure")
    teams: Mapped[list["Team"]] = relationship(back_populates="structure")

    async def __admin_repr__(self, request: Request) -> str:
        """Model's representation in admin.

        Args:
            request (_type_): Request instance

        Returns:
            str: Model's string representation
        """

        return f"{self.name}"
