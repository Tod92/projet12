from datetime import date
from sqlalchemy import ForeignKey, String, Integer, Date
from sqlalchemy.orm import relationship, mapped_column
from src.models.dbengine import Base, CRUDMixin
from src.models.status import Status
from src.models.event import Event



class Contract(Base, CRUDMixin):
    """
    Table contract related to Client (many-to-one) and Event (one-to-one)
    """
    __tablename__ = "contract"
    id = mapped_column(Integer, primary_key=True)
    description = mapped_column(String(500), nullable=False)
    totalAmount = mapped_column(Integer)
    remainingAmount = mapped_column(Integer)
    creationDate = mapped_column(Date(), nullable=False, default=date.today())

    status_id = mapped_column(Integer, ForeignKey('status.id'), default=1)
    status = relationship('Status', back_populates='contracts')

    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=True)

    client_id = mapped_column(Integer, ForeignKey('client.id'))
    client = relationship('Client', back_populates='contracts')

    event = relationship('Event', back_populates='contract')

    @property
    def has_event(self):
        if self.event == []:
            return False
        else:
            return True
        
    @property
    def commercialContact(self):
        return self.client.commercialContact

    def __repr__(self):
        return f"<Contract(client={self.client.fullName} company={self.client.company.name} amount={self.totalAmount} status={self.status.name} event={self.has_event} commercial={self.commercialContact.fullName})>"


