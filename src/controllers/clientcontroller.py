from src.models.dbengine import session_scope

from src.views.clientview import ClientView
from src.models.client import Client
from src.controllers.permissions import PermissionsMixin

class ClientController(PermissionsMixin):
    _list_permission = 'isAuth'
    _create_permission = 'isCommercial'
    _update_permission = 'isAffectedTo'

    def __init__(self):
        self.view = ClientView()

    def list(self, option=None):
        self._permission = self._list_permission
        with session_scope() as s:
            self.has_permission(s)
            clients = Client.get_all(s)
            print('nb results : ', len(clients))
            self.view.list_instances(clients)