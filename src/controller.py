from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from src.crud import session_scope
from src.models import Location, User, Role, Company, Client, Status, Contract, Event
from src.views import LocationView, AuthView
from src.population import (
    USER_POPULATION,
    ROLE_POPULATION,
    LOCATION_POPULATION,
    COMPANY_POPULATION,
    CLIENT_POPULATION,
    STATUS_POPULATION,
    CONTRACT_POPULATION,
    EVENT_POPULATION
)
from src.auth import AuthManager
from sqlalchemy import select


PH = PasswordHasher()

def auth_user():
    view = AuthView()
    with session_scope() as s:
        while True:    
            login = view.get_login()
            request = select(User).where(User.firstName == login)
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

def verify_auth():
    email = AuthManager.auth()
    print('logged as : ' + email)

def add_location():
    view = LocationView()
    input = view.run()

    with session_scope() as s:
        location = Location()
        location.address = input
        s.add(location)

