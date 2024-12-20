from starlette_admin.contrib.sqla import Admin, ModelView

from core.models import Relation, Role, Structure, Team, User, db_connector

admin = Admin(engine=db_connector.engine)

admin.add_view(ModelView(User))
admin.add_view(ModelView(Role))
admin.add_view(ModelView(Relation))
admin.add_view(ModelView(Structure))
admin.add_view(ModelView(Team))
