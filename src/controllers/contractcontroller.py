from src.models.dbengine import session_scope

from src.views.contractview import ContractView
from src.models.contract import Contract
from src.models.client import Client
from src.models.status import Status

from src.controllers.permissions import PermissionsMixin

import logging


class ContractController(PermissionsMixin):
    _table_name = 'contract'
    _list_permissions = ['isAuth']
    _create_permissions = ['isGestion']
    _update_permissions = ['isAffectedToClient', 'isGestion']
    _updatables = ['description', 'totalAmount', 'remainingAmount', 'status', 'client']

    def __init__(self):
        self.view = ContractView()

    def list(self, option=None):
        self._permissions = self._list_permissions
        with session_scope() as s:
            self.has_permission(s)
            contracts = Contract.get_all(s)
            if option == 'topay':
                contracts = list(filter(lambda x: x.isnt_paid(), contracts))
            elif option == 'tosign':
                contracts = list(filter(lambda x: x.status.id == 1, contracts))
            self.view.list_instances(contracts)

    def create(self, option=None):
        self._permissions = self._create_permissions
        with session_scope() as s:
            self.has_permission(s)
            self.view.creation_starting(self._table_name)
            contract = Contract()
            # Prompting client for contract
            clients = Client.get_all(s)
            contract.client_id = self.view.list_instances(clients, prompt=True)
            # Prompting contract informations
            contract.description = self.view.get_str('Description', max_length=500)
            contract.totalAmount = self.view.get_int('Total amount')
            contract.remainingAmount = self.view.get_int('Remaining amount')
            # Affecting app user to new contract
            contract.user_id = self._user.id
            # Creating entry
            s.add(contract)

    def update(self, option=None):
        with session_scope() as s:
            # First permission check for list
            self._permissions = self._list_permissions
            self.has_permission(s)
            contracts = Contract.get_all(s)
            choice = self.view.list_instances(contracts, prompt=True)
            self.instance = contracts[choice-1]
            # Second permission check for update
            self._permissions = self._update_permissions
            self.has_permission(s)
            choice = self._updatables[self.view.pick_in_attr(self._updatables, self.instance)]
            if choice == 'description':
                self.instance.description = self.view.get_str('Description', max_length=500)
            elif choice == 'totalAmount':
                self.instance.totalAmount = self.view.get_int('Total amount')
            elif choice == 'remainingAmount':
                self.instance.remainingAmount = self.view.get_int('Remaining amount')
            elif choice == 'client':
                clients = Client.get_all(s)
                self.instance.client_id = self.view.list_instances(clients, prompt=True)
            elif choice == 'status':
                statuses = Status.get_all(s)
                self.instance.status_id = self.view.list_instances(statuses, prompt=True)
                # Logging status update (commit needed before log)
                s.commit()
                logging.info(f'Status Updated for contract : {self.instance}')
