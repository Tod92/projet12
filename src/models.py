from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    Date,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import date, datetime


Base = declarative_base()

# class Parent(Base):
#     """
#     for tests
#     """
#     __tablename__ = 'parent'
#     id = Column(Integer, primary_key=True)
#     firstName = Column(String(50), nullable=False)
#     lastName = Column(String(50), nullable=False)
    
#     def __repr__(self):
#         return "<Parent(firstName='{}', LastName='{}')>"\
#                 .format(self.firstName, self.lastName)


# class Enfant(Base):
#     """test"""
#     __tablename__ = 'enfant'
#     id = Column(Integer, primary_key=True)
#     firstName = Column(String(50), nullable=False)
#     lastName = Column(String(50), nullable=False)
    
#     parent_id = Column(Integer, ForeignKey('parent.id'), nullable=False)

#     def __repr__(self):
#         return "<Enfant(firstName='{}', LastName='{}')>"\
#                 .format(self.firstName, self.lastName)



class User(Base):
    """ commercial / support / gestion """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)

class Role:
    pass

class Client(Base):
    """
    Table client related to Company (many-to-one) and Contract (one-to-many)
    """
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    creationDate = Column(Date(), nullable=False, default=date.today())
    lastUpdateDate = Column(Date(), nullable=False, default=date.today())

    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship('Company', back_populates='clients')

    contracts = relationship('Contract', back_populates='client')

    @property
    def fullName(self):
        return self.firstName + ' ' + self.lastName


class Event(Base):
    """
    Table event related to Location (many-to-one) and Contract (one-to-one)
    """
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    location_id = Column(Integer, ForeignKey('location.id'))
    


class Contract(Base):
    """
    Table contract related to Client (many-to-one) and Event (one-to-one)
    """
    __tablename__ = "contract"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    client_id = Column(Integer, ForeignKey('client.id'))
    client = relationship('Client', back_populates='contracts')

    
class Company(Base):
    """
    Table company related to Client (one-to-many) and Location (one-to-one)
    """
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    clients = relationship('Client', back_populates='company')

    location_id = Column(Integer, ForeignKey('location.id'))


class Location(Base):
    """
    Table location related to Company (one-to-one) and/or Event (one-to-many)
    """
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    address = Column(String(150), nullable=False)

        





