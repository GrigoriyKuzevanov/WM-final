from starlette.requests import Request
from starlette_admin.contrib.sqla import ModelView


class UserView(ModelView):
    fields = ["id", "email", "info", "role", "is_active", "is_superuser"]
    page_size = 5

    def can_create(self, request: Request) -> bool:
        return False
