from .. import models, schema,utils
from fastapi import Body, FastAPI,Response, status,HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import engine , Sessionlocal,get_db
from typing import Optional, List

router = APIRouter(

    tags= ['For Users']
)

@router.post("/login", status_code= status.HTTP_201_CREATED,response_model= schema.loginout)
def User_login(user: schema.Userlogin, db: Session = Depends(get_db)):
    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password #update pydatic user model
    new_users = models.User_login(**user.dict())
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    return  new_users 

@router.get("/Usersinfo/{id}",response_model= schema.loginout)  
def get_user(id: int, db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM "users" WHERE id = %s """, (str(id),))
    #user = cursor.fetchone()
    user = db.query(models.User_login).filter(models.User_login.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} was not found.")
        
    return user  
