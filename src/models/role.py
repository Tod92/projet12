from argon2 import PasswordHasher
from sqlalchemy import ForeignKey, String, Integer, select
from sqlalchemy.orm import relationship, mapped_column
from src.models.dbengine import Base, CRUDMixin


class Role(Base, CRUDMixin):
    """
    Role to manage permissions commercial / support / gestion 
    """
    __tablename__ = 'role'
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False, unique=True)

    users = relationship('User', back_populates='role')
     
    def __repr__(self):
        return f"<Role({self.name})>"
                
