import sys
sys.path.append("..") # Adds higher directory to python modules path.
from config import USER_POPULATION


from src.crud import session_scope
from src.models import Location, User
from src.views import LocationView

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
            user.firstName = u['firstName']
            user.lastName = u['lastName']
            user.email = u['email']
            s.add(user)