from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from src.crud import session_scope, PermissionManager
from src.models import Location, User, Role, Company, Client, Status, Contract, Event
from src.views import LocationView, AuthView, ClientView, ContractView, EventView

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
        



    def add_location(self):
        view = LocationView()
        input = view.run()

        with session_scope() as s:
            location = Location()
            location.address = input
            s.add(location)

    def list_clients(self):
        view = ClientView()
        _permission = 'isCommercial'
        login = self.get_logged_user_or_ask_login()
        with session_scope() as s:
            request = select(User).where(User.login == login)
            user = s.scalars(request).first()
            PM = PermissionManager(_permission, user)
            if PM.has_permission() == False:
                view.permission_denied()
                exit()

            request = select(Client)
            clients = s.scalars(request).all()
            for c in clients:
                view.detail(c)

    def list_contracts(self):
        user = self.get_logged_user_or_ask_login()
        view = ContractView()
        with session_scope() as s:
            request = select(Contract)
            contracts = s.scalars(request).all()
            for c in contracts:
                view.detail(c)

    def list_events(self):
        user = self.get_logged_user_or_ask_login()
        view = EventView()
        with session_scope() as s:
            request = select(Event)
            events = s.scalars(request).all()
            for e in events:
                view.detail(e)


