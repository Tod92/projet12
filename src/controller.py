from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from src.crud import session_scope
from src.models import Location, User, Role, Company, Client, Status, Contract
from src.views import LocationView, AuthView
from src.populator import (
    USER_POPULATION,
    ROLE_POPULATION,
    LOCATION_POPULATION,
    COMPANY_POPULATION,
    CLIENT_POPULATION,
    STATUS_POPULATION,
    CONTRACT_POPULATION
)

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
        # Role
        for r in ROLE_POPULATION:
            role = Role()
            role.name = r['name']
            role.id = r['id']
            s.add(role)
        # User
        for u in USER_POPULATION:
            user = User()
            user.password = PH.hash(u['password'])
            user.firstName = u['firstName']
            user.lastName = u['lastName']
            user.email = u['email']
            user.id = u['id']
            user.role_id = u['role_id']
            s.add(user)
        # Location
        for l in LOCATION_POPULATION:
            location = Location()
            location.address = l['address']
            location.id = l['id']
            s.add(location)
    with session_scope() as s:
        # Company:
        for c in COMPANY_POPULATION:
            company = Company()
            company.id = c['id']
            company.name = c['name']
            company.location_id = c['location_id']
            s.add(company)
    with session_scope() as s:
        # Client:
        for c in CLIENT_POPULATION:
            client = Client()
            client.id = c['id']
            client.firstName = c['firstName']
            client.lastName = c['lastName']
            client.email = c['email']
            client.phone = c['phone']         
            client.company_id = c['company_id']
            s.add(client)
    with session_scope() as s:
        # Status:
        for stat in STATUS_POPULATION:
            status = Status()
            status.id = stat['id']
            status.name = stat['name']
            s.add(status)
    with session_scope() as s:
        # Contract:
        for c in CONTRACT_POPULATION:
            contract = Contract()
            contract.id = c['id']
            contract.description = c['description']
            contract.totalAmount = c['totalAmount']
            contract.remainingAmount = c['remainingAmount']
            contract.client_id = c['client_id']

            s.add(contract)


            