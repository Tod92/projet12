from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from src.crud import session_scope, PermissionManager
from src.models import Location, User, Role, Company, Client, Status, Contract, Event
from src.views import View, LocationView, AuthView, ClientView, ContractView, EventView, UserView

from src.auth import AuthManager
from sqlalchemy import select


PH = PasswordHasher()


class Controller:
    """
    Main app controller
    """
    def auth_user(self):
        """
        Asks user for login and password then gets him authenticated with jwt token in json file 
        """
        view = AuthView()
        with session_scope() as s:
            while True:    
                login = view.get_login()
                user = self.get_user(session=s, login=login)
                if user:
                    break
                view.not_found()
            while True:
                password = view.get_password()
                try:
                    PH.verify(user.password, password)
                    break
                except VerifyMismatchError:
                    view.bad_password()
            success = AuthManager.gen_token(user)
            view.success(success)
            return user.login

    def verify_auth(self):
        """
        Verify validity of jwt token in json file.
        Returns user login
        """
        view = AuthView()
        login = AuthManager.auth()
        if login:
            view.valid_token(login)
            return login
        else:
            view.invalid_token()

    def get_logged_user_or_ask_login(self):
        """
        Check user credentials and ask for loggin if token expired or not found
        Returns user instance
        """
        login = self.verify_auth()
        while login == None:
            login = self.auth_user()
        return login
        

    def create(self, table=None):
        """
        Creates objects in table
        Must be in ['client', 'contract', 'event']
        """
        # Targeting class and loading associated permission and view
        if table == 'user':
            _permission = 'isGestion'
            view = UserView()
        elif table == 'client':
            _permission = 'isCommercial'
            view = ClientView()
        elif table == 'contract':
            _permission = 'isGestion'
            view = ContractView()
        elif table == 'event':
            _permission = 'isCommercial'
            view = EventView()
        else:
            view = View()
            view.not_found(table)
            exit()
        # Authentication process
        login = self.get_logged_user_or_ask_login()
        # Initiatin session
        with session_scope() as s:
            # Loading app user from database
            app_user = self.get_user(session=s, login=login)
            # Permission checking
            PM = PermissionManager(_permission, app_user)
            if PM.has_permission() == False:
                view.permission_denied()
                exit()
            # Targeting class to perform object creation process        
            if table == 'user':
                user = User()
                # Prompting role for user
                roles = s.scalars(select(Role)).all()
                user.role_id = view.pick_in_list(roles)
                # Prompting user informations
                user.firstName, user.lastName, user.login, user.email, user.password = view.get_info()
                # Prompting and hashing password
                user.password = PH.hash(user.password)
                # Creating entry
                s.add(user)
            elif table == 'client':
                client = Client()
                # Prompting company for client
                companies = s.scalars(select(Company)).all()
                client.company_id = view.pick_in_list(companies)
                # Prompting client informations
                client.firstName, client.lastName, client.email, client.phone = view.get_info()
                # Affecting app user to new client
                client.user_id = app_user.id
                # Creating entry
                s.add(client)

            elif table == 'contract':
                contract = Contract()
                # Prompting client for contract
                clients = s.scalars(select(Client)).all()
                contract.client_id = view.pick_client(clients)
                # Prompting contract informations
                contract.description, contract.totalAmount = view.get_info()
                # Creating entry
                s.add(contract)
            elif table == 'event':
                event = Event()
                # Building contract list : app_user must be affected to contracts
                contracts = s.scalars(select(Contract).where(Contract.user_id == app_user.id)).all()
                # Checking contract status is 'signed' and no previous event present in contract
                contracts = [c for c in contracts if c.status.name == 'signed' and c.event_id is None ]
                # Prompting contract for event
                if contracts:
                    event.contract_id = view.pick_in_list(contracts)
                else:
                    view.no_contract_found()
                    exit()
                # Prompting event informations
                event.location_id = self.add_location()
                event.startDate, event.endDate, event.attendees, event.notes = view.get_info()
                # Creating entry
                s.add(event)

        
    def list(self, table=None, option=None):
        """
        Lists objects from table.
        Must be in ['user', 'client', 'contract', 'event']
        """
        _permission = 'isAuth'
        if table == 'user':
            _permission = 'isGestion'
        login = self.get_logged_user_or_ask_login()
        with session_scope() as s:
            view = View()
            # Loading app user from database
            app_user = self.get_user(session=s, login=login)
            # Permission checking
            PM = PermissionManager(_permission, app_user)
            if PM.has_permission() == False:
                view.permission_denied()
                exit()
            # Targeting class to perform objects listing process
            if table == 'client':
                view = ClientView()
                request = select(Client)
                if option == 'mine':
                    request = request.where(Client.user_id == app_user.id)
            elif table == 'user':
                view = UserView()
                request = select(User)
                if option == 'mine':
                    request = request.where(User.id == app_user.id)
            elif table == 'contract':
                view = ContractView()
                request = select(Contract)
                if option == 'mine':
                    request = request.where(Contract.user_id == app_user.id)
            elif table == 'event':
                view = EventView()
                request = select(Event)
                if option == 'mine':
                    request = request.where(Event.user_id == app_user.id)
            # If table not existing
            else:
                view.unknown_object(description=table)
                exit()

            instances = s.scalars(request).all()
            if instances:
                for i in instances:
                    view.detail(i)
            else:
                view.not_found()


    def add_location(self):
        """
        Not to be called directly. Used by other controller methods
        """
        view = LocationView()
        input = view.run()

        with session_scope() as s:
            location = Location()
            location.address = input
            s.add(location)
            return location.id


    def get_user(self, session, login):
        request = select(User).where(User.login == login)
        return session.scalars(request).first()


