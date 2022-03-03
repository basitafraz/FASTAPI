from os import access
from unicodedata import name
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime





class UserBase(BaseModel):
    name: Optional[str] = None
    name_arabic: Optional[str] = None
    description: Optional[str] = None
    description_arabic : Optional[str] = None
    address: Optional[str] = None
    address_arabic : Optional[str] = None
    phone_number : Optional[str] = None 
    status : bool = False
    
    
class UserCreate(UserBase):
    pass
    class Config:
        orm_mode = True

class loginout(BaseModel):
    id : int
    email: str
    created_at : datetime

    class Config:
        orm_mode = True

class User(BaseModel):
    name : str
    created_at : datetime
    id : int
    owner_id: int
    owner: loginout

    class Config:
        orm_mode = True

class Userlogin(BaseModel):
    email : str
    password : str



class Userauth(BaseModel):
    email : str
    password : str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token = str
    token_type = str

class TokenData(BaseModel): 
    id: Optional[str] = None 