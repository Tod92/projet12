import sys
sys.path.append("..") # Adds higher directory to python modules path.
from config import DATABASE_URI

from argon2 import PasswordHasher

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base, Location, User, Role, Company, Client, Status, Contract, Event
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
from contextlib import contextmanager


engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)

PH = PasswordHasher()

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

class PermissionManager:
    """
    Manage role based user permission. May need object instance to check if user affected to it.
    'isAuth' : user is authenticated in app
    'isAffectedTo' : user is reponsable of object instance
    'isGestion' 'isCommercial' 'isSupport' : user has role
    """
    def __init__(self, permission, user) -> None:
        self._permission = permission
        self._user = user

    def has_permission(self, instance=None):
        if self._permission == 'isAuth':
            if self._user:
                return True
        elif self._permission == 'isAffectedTo':
            if instance.user_id == self._user.id:
                return True
        elif self._permission == 'isGestion':
            if self._user.role.name == 'Gestion':
                return True
        elif self._permission == 'isCommercial':
            if self._user.role.name == 'Commercial':
                return True
        elif self._permission == 'isSupport':
            if self._user.role.name == 'Support':
                return True
        return False

def delete_database():
    Base.metadata.drop_all(engine)

    
def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


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
            user.login = u['login']
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
            contract.user_id = c['user_id']
            s.add(contract)
    with session_scope() as s:
        #Event:
        for e in EVENT_POPULATION:
            event = Event()
            event.id = e['id']
            event.name = e['name']
            event.attendees = e['attendees']
            event.notes = e['notes']
            event.contract_id = e['contract_id']
            event.location_id = e['location_id']
            s.add(event)            
