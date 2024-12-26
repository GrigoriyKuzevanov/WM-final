from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from core.model_adapter import ModelAdapter
from meetings.models import Meeting

MM = TypeVar("MM", bound=Meeting)


class MeetingAdapter(ModelAdapter):
    """Adapter class for performing database operations to the Meeting model."""

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the adapter

        Args:
            session (AsyncSession): Async session
        """

        super().__init__(Meeting, session)
