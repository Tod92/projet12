from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    Date,
    DateTime,
    Float,
)
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from datetime import date, datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    firstName = mapped_column(String(50), nullable=False)
    lastName = mapped_column(String(50), nullable=False)
    # Login as 'flas' : 'jbon' for Bond, 'jbou' for Bourne
    login = mapped_column(String(4),nullable=False, unique=True)
    email = mapped_column(String(50), nullable=False, unique=True)
    password = mapped_column(String(200), nullable=False)
    role_id = mapped_column(Integer, ForeignKey('role.id'))
    role = relationship('Role',back_populates='users')
    
    def __repr__(self):
        return "<User(firstName='{}', LastName='{}')>"\
                .format(self.firstName, self.lastName)
    
    @property
    def fullName(self):
        return self.firstName + ' ' + self.lastName
 
class Client(Base):
    """
    Table client related to Company (many-to-one) and Contract (one-to-many)
    """
    __tablename__ = 'client'
    id = mapped_column(Integer, primary_key=True)
    firstName = mapped_column(String(50), nullable=False)
    lastName = mapped_column(String(50), nullable=False)
    email = mapped_column(String(50), nullable=False)
    phone = mapped_column(String(50), nullable=False)
    creationDate = mapped_column(Date(), nullable=False, default=date.today())
    lastUpdateDate = mapped_column(Date(), nullable=False, default=date.today())

    company_id = mapped_column(Integer, ForeignKey('company.id'))
    company = relationship('Company', back_populates='clients')

    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    commercialContact = relationship('User')

    contracts = relationship('Contract', back_populates='client')

    @property
    def fullName(self):
        return self.firstName + ' ' + self.lastName


class Event(Base):
    """
    Table event related to Location (many-to-one) and Contract (one-to-one)
    """
    __tablename__ = 'event'

    def __repr__(self):
        return f"<Event({self.name} start={self.startDate} attendees={self.attendees} \
            location={self.location.address} contract no={contract.id})>"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    startDate = mapped_column(Date(), nullable=False, default=date.today())
    endDate = mapped_column(Date(), nullable=True)
    attendees = mapped_column(Integer, nullable=False)
    notes = mapped_column(String(500), nullable=True)
    location_id = mapped_column(Integer, ForeignKey('location.id'))
    location = relationship('Location', back_populates='events')
    contract_id = mapped_column(Integer, ForeignKey('contract.id'))
    contract = relationship('Contract', back_populates='event')

    supportContact_id = mapped_column(Integer, ForeignKey('user.id'))


class Contract(Base):
    """
    Table contract related to Client (many-to-one) and Event (one-to-one)
    """
    __tablename__ = "contract"

    def __repr__(self):
        return f"<Contract(client={self.client} company={self.client.company.name} \
            amount={self.totalAmount} commercial={self.commercialContact} event={self.event})>"

    id = mapped_column(Integer, primary_key=True)
    description = mapped_column(String(500), nullable=False)
    totalAmount = mapped_column(Integer)
    remainingAmount = mapped_column(Integer)
    creationDate = mapped_column(Date(), nullable=False, default=date.today())
    status_id = mapped_column(Integer, ForeignKey('status.id'), default=1)
    status = relationship('Status', back_populates='contracts')

    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    commercialContact = relationship('User')

    client_id = mapped_column(Integer, ForeignKey('client.id'))
    client = relationship('Client', back_populates='contracts')

    event = relationship('Event', back_populates='contract')


class Status(Base):
    """
    Table for contract's status related to CContract (many-to-one)
    """    
    __tablename__ = "status"

    def __repr__(self):
        return f"<Status({self.name})>"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(20), nullable=False)
    contracts = relationship('Contract', back_populates='status')

class Company(Base):
    """
    Table company related to Client (one-to-many) and Location (one-to-one)
    """
    __tablename__ = 'company'

    def __repr__(self):
        return f"<Company({self.name})>"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)

    clients = relationship('Client', back_populates='company')

    location_id = mapped_column(Integer, ForeignKey('location.id'))


class Location(Base):
    """
    Table location related to Company (one-to-one) and/or Event (one-to-many)
    """
    __tablename__ = 'location'

    def __repr__(self):
        return f"<Location({self.address})>"

    id = mapped_column(Integer, primary_key=True)
    address = mapped_column(String(150), nullable=False)
    events = relationship('Event', back_populates='location')
        
class Role(Base):
    """Role to manage permissions commercial / support / gestion """

    __tablename__ = 'role'
    
    def __repr__(self):
        return f"<Role({self.name})>"
                

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False, unique=True)
    users = relationship('User', back_populates='role')
  




