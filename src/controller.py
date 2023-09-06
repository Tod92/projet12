from src.crud import session_scope
from src.models import Location
from src.views import LocationView

def add_location():
    view = LocationView()
    input = view.run()

    with session_scope() as s:
        location = Location()
        location.address = input
        s.add(location)