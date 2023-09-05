from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from config import DATABASE_URI
from models import Base


from contextlib import contextmanager


engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)


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

# Creation des tables d'après les models, récupérés via le metadata de Base
# Base.metadata.create_all(engine)

# Suppression des tables
# Base.metadata.drop_all(engine)
def delete_database():
    Base.metadata.drop_all(engine)

    
def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


