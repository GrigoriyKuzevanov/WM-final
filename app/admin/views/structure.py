from starlette_admin.contrib.sqla import ModelView


class StructureView(ModelView):
    fields = ["id", "name", "info", "teams", "roles", "relations"]
    sortable_fields = ["name"]
    fields_default_sort = ["id"]
    page_size = 5
