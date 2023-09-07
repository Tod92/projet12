from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

import sys
sys.path.append("..") # Adds higher directory to python modules path.
from config import USER_POPULATION, ROLE_POPULATION


from src.crud import session_scope
from src.models import Location, User, Role
from src.views import LocationView, AuthView

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
                print(user)
                break
            view.not_found()
        while True:
            password = view.get_password()
            try:
                PH.verify(user.password, password)
                print("correct password")
                break
            except VerifyMismatchError:
                print("INCORRECT PASSWORD")
        

def add_location():
    view = LocationView()
    input = view.run()

    with session_scope() as s:
        location = Location()
        location.address = input
        s.add(location)


def populate_database():
    # Une seule session pour rollback si erreur
    with session_scope() as s:
        # Users
        for u in USER_POPULATION:
            user = User()
            user.password = PH.hash(u['password'])
            user.firstName = u['firstName']
            user.lastName = u['lastName']
            user.email = u['email']
            s.add(user)
        # Role
        for r in ROLE_POPULATION:
            role = Role()
            role.name = r['name']
            role.id = r['id']
            s.add(role)
