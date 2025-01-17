from starlette.requests import Request
from starlette_admin.contrib.sqla import ModelView


class WorkTaskView(ModelView):
    fields = [
        "id",
        "name",
        "description",
        "comments",
        "status",
        "complete_by",
        "rate",
        "creator",
        "assignee",
    ]
    fields_default_sort = ["id"]
    page_size = 5

    def can_create(self, request: Request) -> bool:
        return False
