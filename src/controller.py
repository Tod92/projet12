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
    def auth_user(self):
        """
        Asks user for login and password then gets him authenticated with jwt token in json file 
        """
        view = AuthView()
        with session_scope() as s:
            while True:    
                login = view.get_login()
                request = select(User).where(User.login == login)
                user = s.execute(request).first()
                if user:
                    # On recupère un tuple, récuperation de l'instance User seule
                    user = user[0] 
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
        view = AuthView()
        user = None
        login = AuthManager.auth()
        if login:
            view.valid_token()
            with session_scope() as s:
                request = select(User).where(User.login == login)
                user = s.execute(request).first()[0]
                if user:
                    view.is_logged_in(user.fullName)
                    view.is_logged_in(user.role.name)
                    return user.login
                else:
                    view.not_found()
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
        
    def add_user(self):
        _permission = 'isGestion'
        view = UserView()
        login = self.get_logged_user_or_ask_login()
        PM = PermissionManager(_permission, login)
        if PM.has_permission() == False:
            view.permission_denied()
            exit()
        with session_scope() as s:
            user = User()
            roles = s.scalars(select(Role)).all()
            user.role_id = view.pick_role(roles)
            user.firstName, user.lastName, user.login, user.email, user.password = view.get_info()
            user.password = PH.hash(user.password)
            s.add(user)

    def add_client(self):
        _permission = 'isCommercial'
        view = ClientView()

    def create(self, table=None):
        if table == 'user':
            _permission = 'isGestion'
            view = UserView()
        if table == 'contract':
            _permission = 'isGestion'
            view = ContractView()
        if table == 'event':
            _permission = 'isCommercial'
            view = EventView()
        login = self.get_logged_user_or_ask_login()
        PM = PermissionManager(_permission, login)
        if PM.has_permission() == False:
            view.permission_denied()
            exit()
                       
        with session_scope() as s:
            if table == 'user':
                user = User()
                roles = s.scalars(select(Role)).all()
                user.role_id = view.pick_role(roles)
                user.firstName, user.lastName, user.login, user.email, user.password = view.get_info()
                user.password = PH.hash(user.password)
                s.add(user)
            elif table == 'contract':
                contract = Contract()
                clients = s.scalars(select(Client)).all()
                contract.client_id = view.pick_client(clients)
                contract.description, contract.totalAmount = view.get_info()
                s.add(contract)
            elif table == 'event':
                event = Event()
                # Un event se crée à partir d'un contrat signé dont il est responsable
                user = s.scalars(select(User).where(User.login == login)).first()
                contracts = s.scalars(select(Contract).where(Contract.user_id == user.id)).all()
                contracts = [c for c in contracts if c.status.name == 'signed' and c.event_id is None ]

                if contracts:
                    event.contract_id = view.pick_contract(contracts)
                else:
                    view.no_contract_found()
                    exit()


    def add_location(self):
        view = LocationView()
        input = view.run()

        with session_scope() as s:
            location = Location()
            location.address = input
            s.add(location)

    def list(self, table=None):
        _permission = 'isAuth'
        login = self.get_logged_user_or_ask_login()
        PM = PermissionManager(_permission, login)
        if PM.has_permission() == False:
            view = View()
            view.permission_denied()
            exit()
        else:
            with session_scope() as s:
                if table == 'client':
                    view = ClientView()
                    request = select(Client)
                elif table == 'contract':
                    view = ContractView()
                    request = select(Contract)
                elif table == 'event':
                    view = EventView()
                    request = select(Event)
                instances = s.scalars(request).all()
                for i in instances:
                    view.detail(i)




