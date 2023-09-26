import sys
sys.path.append("..") # Adds higher directory to python modules path.
from config import DATABASE_URI

from sqlalchemy import create_engine, select
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError


from contextlib import contextmanager


engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)

Base = declarative_base()

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    # except IntegrityError:
    #     print("--- Error : IntegrityError --- Please verify informations and try again --- Rollback and closing app")
    #     session.rollback()
    #     exit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

class CRUDMixin:
    """
    Class mixin to perform CRUD operation in sql databse
    """
    
    @classmethod
    def get_id(cls, session, id):
        return session.scalars(select(cls).where(cls.id == id)).first()

    @classmethod
    def get_all(cls, session):
        return session.scalars(select(cls).order_by(cls.id)).all()

    @classmethod
    def get_mine(cls, session, user):
        return session.scalars(select(cls).where(cls.user_id == user.id)).all()
        
    @classmethod
    def get_name(cls, session, name):
        return session.scalars(select(cls).where(cls.name == name)).first()

    @classmethod
    def get_role_name(cls, session, role_name):
        return session.scalars(select(cls).where(cls.role.name == role_name)).all()

