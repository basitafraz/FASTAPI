from multiprocessing.managers import Token
from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..import database, schema, models, utils, oauth2
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post('/auth')
def auth(user_credentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
     user = db.query(models.User_login).filter(models.User_login.email == user_credentials.username).first()

     if not user:
         raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"invalid credentials")

     if not utils.verify(user_credentials.password, user.password):
         raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail= f"invalid credentials")


     access_token = oauth2.create_access_token(data = {"user_id" : user.id})
     
     return {"access_token": access_token , "token_type": "bearer"  }
