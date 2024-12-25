from starlette.requests import Request
from starlette_admin.contrib.sqla import ModelView


class UserView(ModelView):
    fields = ["id", "email", "is_active", "is_superuser", "is_verified", "role_id"]
    page_size = 5

    def can_create(self, request: Request) -> bool:
        return False
