from src.models.dbengine import session_scope

from src.views.eventview import EventView
from src.models.event import Event
from src.models.contract import Contract
from src.models.location import Location
from src.controllers.permissions import PermissionsMixin

class EventController(PermissionsMixin):
    _table_name = 'event'
    _list_permissions = ['isAuth']
    _create_permissions = ['isCommercial']
    _update_permissions = ['isAffectedTo']
    _updatables = ['name', 'startDate', 'endDate', 'attendees', 'notes']

    def __init__(self):
        self.view = EventView()

    def list(self, option=None):
        self._permissions = self._list_permissions
        with session_scope() as s:
            self.has_permission(s)
            events = Event.get_all(s)
            self.view.list_instances(events)

    def create(self, option=None):
        self._permissions = self._create_permissions
        with session_scope() as s:
            self.has_permission(s)
            self.view.creation_starting(self._table_name)
            event = Event()
            # Prompting contract for event
            contracts = Contract.get_mine(s, self._user)
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
            # Affecting app user to new event
            event.user_id = self._user.id
            # Creating entry
            s.add(event)

    def update(self, option=None):
        with session_scope() as s:
            # First permission check for list
            self._permissions = self._list_permissions
            self.has_permission(s)
            events = Event.get_all(s)
            choice = self.view.list_instances(events, prompt=True)
            self.instance = events[choice-1]
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
