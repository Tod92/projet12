from datetime import date
from sqlalchemy import ForeignKey, String, Integer, Date
from sqlalchemy.orm import relationship, mapped_column
from src.models.dbengine import Base, CRUDMixin
from src.models.location import Location




class Event(Base, CRUDMixin):
    """
    Table event related to Location (many-to-one) and Contract (one-to-one)
    """
    __tablename__ = 'event'
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

    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    supportContact = relationship('User')

    @property
    def commercialContact(self):
        return self.contract.commercialContact

    def __repr__(self):
        support = None
        if self.supportContact is not None:
            support = self.supportContact.login
        return f"<Event(contract no={self.contract.id} start={self.startDate} attendees={self.attendees} commercialContact={self.commercialContact.login} supportContact={support})>"
