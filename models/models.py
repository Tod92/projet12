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


class User:
    """ commercial / support / gestion """
    pass

class Role:
    pass

class Client:
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


class Event:
    """
    Table event related to Location (many-to-one) and Contract (one-to-one)
    """
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    # TODO


class Contract:
    pass

class Company:
    """
    Table company related to Client (one-to-many) and location (one-to-one)
    """
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    clients = relationship('Client', back_populates='company')

    location_id = Column(Integer, ForeignKey('location.id'))


class Location:
    """
    Table location related to Company (one-to-one) and/or Event (one-to-many)
    """
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    address = Column(String(150), nullable=False)





