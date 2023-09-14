from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import select
import sys
sys.path.append("..") # Adds higher directory to python modules path.

from src.models.dbengine import session_scope
from src.models.user import User
from src.views.userview import UserView

from src.auth import AuthManager


PH = PasswordHasher()

class UserController:
    _create_prompts = ['firstName', 'lastName', 'email', 'login', 'password', 'role']
    _update_prompts = ['firstName', 'lastName', 'email', 'login', 'password', 'role']

    def __init__(self):
        self.view = UserView()

    def login(self):
        with session_scope() as s:
            while True:    
                login = self.view.get_login()
                user = User.get_login(session=s, login=login)
                if user:
                    break
                self.view.not_found()
            while True:
                password = self.view.get_password()
                try:
                    PH.verify(user.password, password)
                    break
                except VerifyMismatchError:
                    view.bad_password()
            success = AuthManager.gen_token(user)
            self.view.success(success)
            return user.login
 
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
        # Initiating session
        with session_scope() as s:
            # Loading app user from database
            app_user = self.get_user(session=s, login=login)
            # Permission checking
            PM = PermissionManager(_permission, app_user)
            if PM.has_permission() == False:
                view.permission_denied()
                exit()
            view.creation_starting(table)
            # Targeting class to perform object creation process        
            if table == 'user':
                user = User()
                # Prompting role for user
                roles = s.scalars(select(Role)).all()
                user.role_id = view.pick_in_list(roles)
                # Prompting user informations
                user.firstName, user.lastName, user.login, user.email, user.password = view.get_info()
                # Hashing password
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
                contract.client_id = view.pick_in_list(clients)
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
        view.creation_completed(table)

    def update(self, table=None, option=None):
        """
        Updates objects in table
        Must be in ['user', 'client', 'contract', 'event']
        """
        with session_scope() as s:
            login = self.get_logged_user_or_ask_login()
            # Loading app user from database
            app_user = self.get_user(session=s, login=login)
            if table == 'user':
                _permission = 'isGestion'
                view = UserView()
                request = select(User).order_by(User.id)
            elif table == 'client':
                _permission = 'isAffectedTo'
                view = ClientView()
                request = select(Client).where(Client.user_id == app_user.id).order_by(Client.id)
            elif table == 'contract':
                _permission = 'isCommercial'
                view = ContractView()
                request = select(Contract).order_by(Contract.id)
            elif table == 'event':
                _permission = 'isGestion'
                view = EventView()
                request = select(Event).order_by(Event.id)
            # If table not existing
            else:
                view = View()
                view.unknown_object(description=table)
                exit()
            # Permission checking
            PM = PermissionManager(_permission, app_user)
            if PM.has_permission() == False:
                view.permission_denied()
                exit()
            # Permission passed. Executing request.
            instances = s.scalars(request).all()
            choice_id = view.pick_in_list(instances)
            if table == 'user':
                _updatables = ['firstName', 'lastName', 'email', 'login', 'password', 'role']
                user = s.scalars(select(User).where(User.id == choice_id)).first()
                # Prompting user to choose attribute to update
                choice = _updatables[view.pick_in_attr(_updatables, user)]
                if choice == 'firstName':
                    user.firstName = view.get_str(choice)
                elif choice == 'lastName':
                    user.firstName = view.get_str(choice)
                elif choice == 'email':
                    user.email = view.get_str(choice)
                elif choice == 'login':
                    user.login = view.get_str(choice)
                elif choice == 'password':
                    user.password = PH.hash(view.get_password())
                elif choice == 'role':
                    roles = s.scalars(select(Role)).all()
                    user.role_id = view.pick_in_list(roles)
            if table == 'client':
                client = s.scalars(select(Client).where(Client.id == choice_id)).first()
                # Another permission check for the specific client instance
                if PM.has_permission(client) == False:
                    view.permission_denied()
                    exit()
                # Prompting user to choose attribute to update
                _updatables = ['firstName', 'lastName', 'email', 'phone', 'company', 'commercialContact']
                choice = _updatables[view.pick_in_attr(_updatables, client)]
                if choice == 'firstName':
                    client.firstName = view.get_str(choice)
                elif choice == 'lastName':
                    client.lastName = view.get_str(choice)
                elif choice == 'email':
                    client.email = view.get_str(choice)
                elif choice == 'phone':
                    client.phone = view.get_str(choice)
                elif choice == 'company':
                    companies = s.scalars(select(Company)).all()
                    client.company_id = view.pick_in_list(companies)
                elif choice == 'commercialContact':
                    # Querying role table to get wanted role id
                    role = s.scalars(select(Role).where(Role.name == 'Commercial')).first()
                    # Lisint only commercial users
                    commercials = s.scalars(select(User).where(User.role_id == role.id)).all()
                    client.user_id = view.pick_in_list(commercials)
            if table == 'contract':
                contract = s.scalars(select(Contract).where(Contract.id == choice_id)).first()
                _updatables = ['description', 'totalAmount', 'remainingAmount', 'status', 'client']
                choice = _updatables[view.pick_in_attr(_updatables, contract)]
                if choice == 'description':
                    contract.description = view.get_str(choice)
                elif choice == 'totalAmount':
                    contract.totalAmount = view.get_int(choice)
                elif choice == 'remainingAmount':
                    contract.remainingAmount = view.get_int(choice)
                elif choice == 'status':
                    statuses = s.scalars(select(Status)).all()
                    contract.status_id = view.pick_in_list(statuses)
                elif choice == 'client':
                    clients = s.scalars(select(Client)).all()
                    contract.client_id = view.pick_in_list(clients)

        view.update_completed()

    def list(self, table=None, option=None):
        """
        Lists objects from table.
        Must be in ['user', 'client', 'contract', 'event']
        """
        with session_scope() as s:
            login = self.get_logged_user_or_ask_login()
            # Loading app user from database
            app_user = self.get_user(session=s, login=login)
            # Targeting class to perform objects listing process
            if table == 'user':
                _permission = 'isGestion'
                view = UserView()
                request = select(User)
                if option == 'mine':
                    request = request.where(User.id == app_user.id)
                request = request.order_by(User.id)
            elif table == 'client':
                _permission = 'isAuth'
                view = ClientView()
                request = select(Client)
                if option == 'mine':
                    request = request.where(Client.user_id == app_user.id)
                request = request.order_by(Client.id)
            elif table == 'contract':
                _permission = 'isAuth'
                view = ContractView()
                request = select(Contract)
                if option == 'mine':
                    request = request.where(Contract.user_id == app_user.id)
                request = request.order_by(Contract.id)
            elif table == 'event':
                _permission = 'isAuth'
                view = EventView()
                request = select(Event)
                if option == 'mine':
                    request = request.where(Event.user_id == app_user.id)
                request = request.order_by(Event.id)
            # If table not existing
            else:
                view = View()
                view.unknown_object(description=table)
                exit()
            # Permission checking
            PM = PermissionManager(_permission, app_user)
            if PM.has_permission() == False:
                view.permission_denied()
                exit()
            # Permission passed. Executing request.
            instances = s.scalars(request).all()
            view.pick_in_list(instances, prompt=False)



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


