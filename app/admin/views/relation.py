from starlette_admin.contrib.sqla import ModelView


class RelationView(ModelView):
    fields = ["id", "structure", "superior", "subordinate"]
    page_size = 5
