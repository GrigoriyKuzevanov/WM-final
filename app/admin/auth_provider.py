import contextlib

from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import LoginFailed

from core.models import db_connector
from users.dependencies.user_manager import get_user_manager
from users.dependencies.users import get_user_db

get_async_session_context = contextlib.asynccontextmanager(db_connector.get_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


class FastApiUsersAuthProvider(AuthProvider):
    """Authentication provider for Starlette-admin using FastAPI-users."""

    async def is_authenticated(self, request: Request) -> bool:
        """Validates each incoming request. Saves user's email getting from
        request.session username (if it exists) to request.state.admin_username.

        Args:
            request (Request): Incoming request

        Returns:
            bool: True if the user is authenticated, False otherwise
        """

        username: str | None = request.session.get("username")

        if username:
            async with get_async_session_context() as session:
                async with get_user_db_context(session) as user_db:
                    async with get_user_manager_context(user_db) as user_manager:
                        user = await user_manager.get_by_email(user_email=username)
                        if user:
                            request.state.admin_username = user.email

                            return True

        return False

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        """Authenticates the user from admin login form and initiate an admin session.

        Args:
            username (str): Username (email) from admin login form
            password (str): Password from admin login form
            remember_me (bool): Not using
            request (Request): Incoming request
            response (Response): Output response

        Raises:
            LoginFailed: If the authentification fails because of invalid user's
            credentials or user is not admin (User.is_superuser == False)

        Returns:
            Response: Redirect response to the admin dashboard
        """

        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.authenticate(
                        OAuth2PasswordRequestForm(username=username, password=password)
                    )

                    if not user:
                        raise LoginFailed(msg="Login failed: invalid user credentials")
                    if not user.is_superuser:
                        raise LoginFailed(
                            msg="Login failed: you must be an administrator to log in"
                        )

                    request.session.update({"username": username})
                    return RedirectResponse(url="/admin", status_code=303)

    async def logout(self, request: Request, response: Response) -> Response:
        """Logs out the user by clearing the session.

        Args:
            request (Request): Incoming request
            response (Response): Output response

        Returns:
            Response: Response object
        """

        request.session.clear()
        return response

    def get_admin_user(self, request: Request) -> AdminUser:
        """Retrieves the authenticated admin username (email) to display in admin.

        Args:
            request (Request): Incoming request

        Returns:
            AdminUser: The authenticated admin user object
        """

        return AdminUser(username=request.state.admin_username)


auth_provider = FastApiUsersAuthProvider()
