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


class User:
    """ commercial / support / gestion """
    pass

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


class Event(Base):
    """
    Table event related to Location (many-to-one) and Contract (one-to-one)
    """
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    


class Contract(Base):
    """
    Table contract related to Client (many-to-one) and Event (one-to-one)
    """
    __tablename__ = "contract"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
 

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





