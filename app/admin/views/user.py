from starlette_admin.contrib.sqla import ModelView


class UserView(ModelView):
    fields = ["id", "email"]
