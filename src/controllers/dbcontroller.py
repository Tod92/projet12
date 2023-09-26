import json
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from config import POPULATION_FILE

from src.models.dbengine import Base, engine, session_scope
from src.models.user import User
from src.models.client import Client
from src.models.contract import Contract
from src.models.event import Event
from src.models.company import Company
from src.models.location import Location
from src.models.role import Role
from src.models.status import Status





class DbController:

    def init_tables(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def populate_database(self):
        with open(POPULATION_FILE) as f:
            populations = json.load(f)
        with session_scope() as s:
            for r in populations["role"]:
                role = Role()
                role.name = r['name']
                s.add(role)
                s.commit()
            for u in populations['user']:
                user = User()
                user.set_password(u['password'])
                user.firstName = u['firstName']
                user.lastName = u['lastName']
                user.login = u['login']
                user.email = u['email']
                user.role_id = u['role_id']
                s.add(user)               
            for l in populations["location"]:
                location = Location()
                location.address = l['address']
                s.add(location)
                s.commit()
            for c in populations['company']:
                company = Company()
                company.name = c['name']
                company.location_id = c['location_id']
                s.add(company)
            for c in populations['client']:
                client = Client()
                client.firstName = c['firstName']
                client.lastName = c['lastName']
                client.email = c['email']
                client.phone = c['phone']         
                client.company_id = c['company_id']
                client.user_id = c['user_id']
                s.add(client)
            for st in populations['status']:
                status = Status()
                status.name = st['name']
                s.add(status)
            for c in populations['contract']:
                contract = Contract()
                contract.description = c['description']
                contract.totalAmount = c['totalAmount']
                contract.remainingAmount = c['remainingAmount']
                contract.client_id = c['client_id']
                contract.user_id = c['user_id']
                s.add(contract)
            for e in populations['event']:
                event = Event()
                event.name = e['name']
                event.attendees = e['attendees']
                event.notes = e['notes']
                event.contract_id = e['contract_id']
                event.location_id = e['location_id']
                s.add(event)            
