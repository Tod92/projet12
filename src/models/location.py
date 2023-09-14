from argon2 import PasswordHasher
from sqlalchemy import ForeignKey, String, Integer, select
from sqlalchemy.orm import relationship, mapped_column
from src.models.dbengine import Base, CRUDMixin


class Location(Base, CRUDMixin):
    """
    Table location related to Company (one-to-one) and/or Event (one-to-many)
    """
    __tablename__ = 'location'
    id = mapped_column(Integer, primary_key=True)
    address = mapped_column(String(150), nullable=False)
    events = relationship('Event', back_populates='location')
   
    def __repr__(self):
        return f"<Location({self.address})>"
