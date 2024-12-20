from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base_model import Base

if TYPE_CHECKING:
    from .structure import Structure


class Team(Base):
    """A class for represtation teams table in the database"""

    __tablename__ = "teams"

    name: Mapped[str] = mapped_column(nullable=False)
    structure_id: Mapped[int] = mapped_column(
        ForeignKey("structures.id", ondelete="CASCADE"), nullable=False
    )

    structure: Mapped["Structure"] = relationship("Structure", back_populates="teams")
