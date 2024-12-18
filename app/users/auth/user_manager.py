import logging

from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from core.config import settings
from users.models import User

logger = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """A class for users managment logic"""

    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
        self, user: User, request: Request | None = None
    ) -> None:
        """Perform logic after successful user registration.

        Args:
            user (User): Registered user
            request (Request | None): Fastapi request object. Default to None
        """

        logger.warning("User %r has registered.", user.id)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        """Perform logic after successful forgot password request.

        Args:
            user (User): The user that forgot its password
            token (str): The forgot password token
            request (Request | None): Fastapi request object. Default to None
        """

        logger.warning(
            "User %r has forgot their password. Reset token: %r", user.id, token
        )

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        """Perform logic after successful verification request.

        Args:
            user (User): The user to verify
            token (str): The verification token
            request (Request | None): Fastapi request object. Default to None
        """

        logger.warning(
            "Verification requested for user %r. Verification token: %r", user.id, token
        )
