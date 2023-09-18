
from datetime import date
from sqlalchemy import ForeignKey, String, Integer, Date
from sqlalchemy.orm import relationship, mapped_column
from src.models.dbengine import Base, CRUDMixin
from src.models.company import Company
from src.models.contract import Contract



class Client(Base, CRUDMixin):
    """
    Table client related to Company (many-to-one) and Contract (one-to-many)
    """
    __tablename__ = 'client'
    id = mapped_column(Integer, primary_key=True)
    firstName = mapped_column(String(50), nullable=False)
    lastName = mapped_column(String(50), nullable=False)
    email = mapped_column(String(50), nullable=False)
    phone = mapped_column(Integer, nullable=False)
    creationDate = mapped_column(Date(), nullable=False, default=date.today())
    lastUpdateDate = mapped_column(Date(), nullable=False, default=date.today())

    company_id = mapped_column(Integer, ForeignKey('company.id'))
    company = relationship('Company', back_populates='clients')

    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    commercialContact = relationship('User')

    contracts = relationship('Contract', back_populates='client')

    def __repr__(self):
        return f"<Client({self.fullName} company={self.company.name} commercial={self.commercialContact})>"

    @property
    def fullName(self):
        return self.firstName + ' ' + self.lastName
