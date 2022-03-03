from cgitb import text
from unicodedata import name
from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer,String, BOOLEAN
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class User_data(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, nullable=False)
    name = Column(String, nullable=False)
    name_arabic = Column(String, nullable=True)
    description = Column(String, nullable=True)
    description_arabic = Column(String, nullable=True)
    address = Column(String, nullable=True)
    address_arabic = Column(String, nullable=True) 
    phone_number = Column(String, nullable= True)
    email = Column(String, nullable= False) 
    status = Column(BOOLEAN, server_default ="TRUE", nullable=True)       
    created_at = Column(TIMESTAMP(timezone = True), nullable=False, server_default=text('now()'))  
    owner_id = Column(Integer, ForeignKey("user_login.id", ondelete="CASCADE"), nullable= False)
    owner = relationship("User_login")

class User_login(Base):
    __tablename__ = "user_login"

    email = Column(String, nullable= False, unique= True)    
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key= True, nullable=False)
    created_at = Column(TIMESTAMP(timezone = True), nullable=False, server_default=text('now()'))
    


