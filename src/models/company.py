from argon2 import PasswordHasher
from sqlalchemy import ForeignKey, String, Integer, select
from sqlalchemy.orm import relationship, mapped_column
from src.models.dbengine import Base, CRUDMixin


class Company(Base, CRUDMixin):
    """
    Table company related to Client (one-to-many) and Location (one-to-one)
    """
    __tablename__ = 'company'
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)

    clients = relationship('Client', back_populates='company')

    location_id = mapped_column(Integer, ForeignKey('location.id'))

    def __repr__(self):
        return f"<Company({self.name})>"
