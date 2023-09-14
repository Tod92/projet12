from argon2 import PasswordHasher
from sqlalchemy import ForeignKey, String, Integer, select
from sqlalchemy.orm import relationship, mapped_column
from src.models.dbengine import Base, CRUDMixin
from src.models.role import Role
from src.models.client import Client

PH = PasswordHasher()

class User(Base, CRUDMixin):
    __tablename__ = 'user'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    firstName = mapped_column(String(50), nullable=False)
    lastName = mapped_column(String(50), nullable=False)
    # Login as 'flas' : 'jbon' for Bond, 'jbou' for Bourne
    login = mapped_column(String(4),nullable=False, unique=True)
    email = mapped_column(String(50), nullable=False, unique=True)
    password = mapped_column(String(200), nullable=False)
    role_id = mapped_column(Integer, ForeignKey('role.id'))
    role = relationship('Role', back_populates='users')
    clients = relationship('Client', back_populates='commercialContact')

    def __repr__(self):
        return "<User({} login={} role={})>"\
                .format(self.fullName, self.login, self.role.name)
    
    @property
    def user_id(self):
        return self.id
    
    @property
    def fullName(self):
        return self.firstName + ' ' + self.lastName
    
    @classmethod
    def get_from_login(cls, session, login):
        return session.scalars(select(cls).where(cls.login == login)).first()        

    def set_password(self, password):
        self.password = PH.hash(password)
        return True







