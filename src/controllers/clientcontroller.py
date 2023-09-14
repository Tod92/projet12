from src.views.clientview import ClientView
from src.controllers.usercontroller import UserController
from src.models.dbengine import session_scope
from src.models.client import Client


class ClientController:
    _list_permission = 'IsAuth'
    _create_permission = 'IsCommercial'
    _update_permission = 'isAffectedTo'

    def __init__(self):
        self.view = ClientView()

    def list(self, option=None):
        with session_scope() as s:
            user_controller = UserController()
            app_user = user_controller.get_authenticated_user(s)
            print(app_user)
            clients = Client.get_all(s)
            print(len(clients))