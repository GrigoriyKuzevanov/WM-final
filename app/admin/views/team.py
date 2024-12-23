from starlette_admin.contrib.sqla import ModelView


class TeamView(ModelView):
    fields = ["id", "name", "structure"]
    sortable_fields = ["name"]
    page_size = 5
