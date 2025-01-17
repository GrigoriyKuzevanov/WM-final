from fastapi_users import FastAPIUsers

from users.models import User

from .backend import redis_authentication_backend
from .user_manager import get_user_manager

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [redis_authentication_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
