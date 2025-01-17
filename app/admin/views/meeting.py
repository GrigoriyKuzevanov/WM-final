from starlette_admin.contrib.sqla import ModelView


class MeetingView(ModelView):
    fields = ["id", "topic", "info", "meet_datetime", "creator", "users"]
    page_size = 5
