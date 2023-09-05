from crud import session_scope, recreate_database
from models import Parent, Enfant
import json



# client = Client(
#     firstName='John',
#     lastName='Ouik',
#     email='john.ouik@gmail.com',
#     phone='0146238128'
# )

parent = Parent(
    firstName='Omer',
    lastName='Simpson'
)

enfant = Enfant(
    firstName='Bart',
    lastName='Simpson'
)
recreate_database()


with session_scope() as s:
    s.add(parent)

with session_scope() as s:
    omer = s.query(Parent).filter_by(firstName='Omer').first()
    print(omer)
    enfant.parent_id = omer.id
    s.add(enfant)



