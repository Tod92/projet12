from src.models.dbengine import session_scope

from src.views.eventview import EventView
from src.models.event import Event
from src.models.client import Client
from src.models.role import Role
from src.models.location import Location
from src.controllers.permissions import PermissionsMixin

class EventController(PermissionsMixin):
    _table_name = 'event'
    _list_permissions = ['isAuth']
    _create_permissions = ['isCommercial']
    _update_permissions = ['isAffectedToClient', 'isGestion']
    _updatables = ['name', 'startDate', 'endDate', 'attendees', 'notes']

    def __init__(self):
        self.view = EventView()

    def list(self, option=None):
        self._permissions = self._list_permissions
        with session_scope() as s:
            self.has_permission(s)
            if option == 'mine':
                events = Event.get_mine(s, self._user)
            else:    
                events = Event.get_all(s)
            if option == 'nosupport':
                events = list(filter(lambda x: x.user_id == None, events))
            self.view.list_instances(events)

    def create(self, option=None):
        self._permissions = self._create_permissions
        with session_scope() as s:
            self.has_permission(s)
            self.view.creation_starting(self._table_name)
            event = Event()
            # Prompting contract for event
            contracts = []
            clients = Client.get_mine(s, self._user)
            for cl in clients:
                for co in cl.contracts:
                    contracts.append(co)
            # Filtering to get only signed contracts
            contracts = list(filter(lambda x: x.status.id == 2, contracts))
            # Filtering contracts with non existing event
            contracts = list(filter(lambda x: x.has_event is False, contracts))
            event.contract_id = self.view.list_instances(contracts, prompt=True)
            # Prompting location for event
            locations = Location.get_all(s)
            event.location_id = self.view.list_instances(locations, prompt=True)
            # Prompting event informations
            event.name = self.view.get_str('name', max_length=100)
            event.startDate = self.view.get_date('Please enter start date')
            event.endDate = self.view.get_date('Please enter end date')
            event.attendees = self.view.get_int('number of attendees')
            event.notes = self.view.get_str('notes', max_length=500)
            # Creating entry
            s.add(event)

    def update(self, option=None):
        """
        Update will differ wether user is affected commercial or gestion
        Commercial will be able to update everything but affected support user
        """
        with session_scope() as s:
            # First permission check for list
            self._permissions = self._list_permissions
            self.has_permission(s)
            if self._user.role.name == 'Commercial':
                clients = Client.get_mine(s, self._user)
                contracts = []
                for cl in clients:
                    for co in cl.contracts:
                        contracts.append(co)
                events = []
                for co in contracts:
                    if co.event:
                        print(co.event)
                        events.append(co.event[0])
            elif self._user.role.name == 'Gestion':
                events = Event.get_all(s)
                # Gestion user can affect support user to event
                self._updatables.append('user_id')
            else:
                events = Event.get_all(s)

            choice = self.view.list_instances(events, prompt=True)
            self.instance = events[choice-1]
            # Second permission check for update
            self._permissions = self._update_permissions
            self.has_permission(s)
            choice = self._updatables[self.view.pick_in_attr(self._updatables, self.instance)]
            if choice == 'name':
                self.instance.name = self.view.get_str('Name', max_length=100)
            elif choice == 'startDate':
                self.instance.startDate = self.view.get_date('Please enter start date')
            elif choice == 'endDate':
                self.instance.endDate = self.view.get_date('Please enter end date')
            elif choice == 'attendees':
                self.instance.attendees = self.view.get_int('Number of attendees')
            elif choice == 'notes':
                self.instance.notes = self.view.get_str('Notes', max_length=500)
            elif choice == 'user_id':
                # Listing only support users
                role = Role.get_name(s, 'Support')
                supports = role.users
                self.instance.user_id = self.view.list_instances(supports, prompt=True)
            
