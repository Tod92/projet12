from src.models.dbengine import session_scope

from src.views.clientview import ClientView
from src.models.client import Client
from src.models.company import Company
from src.models.role import Role

from src.controllers.permissions import PermissionsMixin

class ClientController(PermissionsMixin):
    _table_name = 'client'
    _list_permissions = ['isAuth']
    _create_permissions = ['isCommercial']
    _update_permissions = ['isAffectedTo']
    _updatables = ['firstName', 'lastName', 'email', 'phone', 'company', 'commercialContact']

    def __init__(self):
        self.view = ClientView()

    def list(self, option=None):
        self._permissions = self._list_permissions
        with session_scope() as s:
            self.has_permission(s)
            clients = Client.get_all(s)
            self.view.list_instances(clients)

    def create(self, option=None):
        self._permissions = self._create_permissions
        with session_scope() as s:
            self.has_permission(s)
            self.view.creation_starting(self._table_name)
            client = Client()
            # Prompting company for client
            companies = Company.get_all(s)
            client.company_id = self.view.list_instances(companies, prompt=True)
            # Prompting client informations
            client.firstName = self.view.get_str('First Name', max_length=50)
            client.lastName = self.view.get_str('Last Name', max_length=50) 
            client.email  = self.view.get_str('Email', max_length=50)
            client.phone = self.view.get_int('Phone')
            # Affecting app user to new client
            client.user_id = self._user.id
            # Creating entry
            s.add(client)

    def update(self, option=None):
        with session_scope() as s:
            # First permission check for list
            self._permissions = self._list_permissions
            self.has_permission(s)
            clients = Client.get_all(s)
            choice = self.view.list_instances(clients, prompt=True)
            self.instance = clients[choice-1]
            # Second permission check for update
            self._permissions = self._update_permissions
            self.has_permission(s)
            choice = self._updatables[self.view.pick_in_attr(self._updatables, self.instance)]
            if choice == 'firstName':
                self.instance.firstName = self.view.get_str('First Name', max_length=50)
            elif choice == 'lastName':
                self.instance.lastName = self.view.get_str('Last Name', max_length=50)
            elif choice == 'email':
                self.instance.email = self.view.get_str('Email', max_length=50)
            elif choice == 'phone':
                self.instance.phone = self.view.get_int('Phone')
            elif choice == 'company':
                companies = Company.get_all(s)
                self.instance.company_id = self.view.list_instances(companies, prompt=True)
            elif choice == 'commercialContact':
                # Listing only commercial users
                role = Role.get_name(s, 'Commercial')
                commercials = role.users
                self.instance.user_id = self.view.list_instances(commercials, prompt=True)
