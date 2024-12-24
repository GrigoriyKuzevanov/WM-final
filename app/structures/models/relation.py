from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.base_model import Base

if TYPE_CHECKING:
    from .structure import Role, Structure


class Relation(Base):
    """A class for represtation relations table in the database"""

    __tablename__ = "relations"

    superior_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"), nullable=False
    )
    subordinate_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"), nullable=False
    )
    structure_id: Mapped[int] = mapped_column(
        ForeignKey("structures.id", ondelete="CASCADE"), nullable=False
    )
    structure: Mapped["Structure"] = relationship(
        "Structure", back_populates="relations"
    )

    superior: Mapped["Role"] = relationship(
        foreign_keys=[superior_id], back_populates="superiors"
    )
    subordinate: Mapped["Role"] = relationship(
        foreign_keys=[subordinate_id], back_populates="subordinates"
    )

    __table_args__ = (
        UniqueConstraint(
            "superior_id", "subordinate_id", "structure_id", name="uq_role_hierarchy"
        ),
    )
