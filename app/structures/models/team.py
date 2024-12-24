from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request

from core.models.base_model import Base

if TYPE_CHECKING:
    from .structure import Structure


class Team(Base):
    """A class for represtation teams table in the database"""

    __tablename__ = "teams"

    name: Mapped[str] = mapped_column(nullable=False)
    info: Mapped[str]

    structure_id: Mapped[int] = mapped_column(
        ForeignKey("structures.id", ondelete="CASCADE"), nullable=False
    )

    structure: Mapped["Structure"] = relationship("Structure", back_populates="teams")

    async def __admin_repr__(self, request: Request) -> str:
        """Model's representation in admin.

        Args:
            request (_type_): Request instance

        Returns:
            str: Model's string representation
        """

        return f"{self.name}"
