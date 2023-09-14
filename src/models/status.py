from argon2 import PasswordHasher
from sqlalchemy import ForeignKey, String, Integer, select
from sqlalchemy.orm import relationship, mapped_column
from src.models.dbengine import Base, CRUDMixin


class Status(Base, CRUDMixin):
    """
    Table for contract's status related to Contract (many-to-one)
    """    
    __tablename__ = "status"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(20), nullable=False)
    contracts = relationship('Contract', back_populates='status')

    def __repr__(self):
        return f"<Status({self.name})>"
