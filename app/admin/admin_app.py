from starlette_admin.contrib.sqla import Admin

from core.models import Meeting, Relation, Role, Structure, User, db_connector

from .auth_provider import auth_provider
from .views import MeetingView, RelationView, RoleView, StructureView, UserView

admin = Admin(engine=db_connector.engine, auth_provider=auth_provider, title="Teams")

admin.add_view(UserView(User, label="Пользователи"))
admin.add_view(RoleView(Role, label="Роли"))
admin.add_view(RelationView(Relation, label="Иерархия"))
admin.add_view(StructureView(Structure, label="Структуры"))
admin.add_view(MeetingView(Meeting, label="Встречи"))
