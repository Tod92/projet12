from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from src.crud import session_scope
from src.models import Location, User, Role, Company, Client, Status, Contract, Event
from src.views import LocationView, AuthView

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
                    return user
                else:
                    view.not_found()
        else:
            view.invalid_token()


    def add_location(self):
        view = LocationView()
        input = view.run()

        with session_scope() as s:
            location = Location()
            location.address = input
            s.add(location)

