from starlette_admin.contrib.sqla import ModelView


class RoleView(ModelView):
    fields = ["id", "name", "info", "users", "structure"]
    sortable_fields = ["name"]
    page_size = 5
