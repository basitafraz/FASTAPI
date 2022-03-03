from sqlalchemy import delete
from .. import models, schema,utils, oauth2
from fastapi import Body, FastAPI,Response, status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine , Sessionlocal,get_db
from typing import Optional, List

router = APIRouter(
    prefix= "/Users",
    tags= ['USER']
   
)


@router.get("/",response_model=List [schema.User])
def get_users(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM "users" """)
    #user = cursor.fetchall()
    
    users = db.query(models.User_data).filter(models.User_data.owner_id == current_user.id).all()
    
    return  users

@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schema.User)
async def add_user(post: schema.UserCreate, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO "users" (name,email) VALUES(%s,%s)  RETURNING * """,
    #(post.Name, post.Email))
    
    #new_user = cursor.fetchone()
    #conn.commit()
    
    users = models.User_data(owner_id = current_user.id, ** post.dict())
    db.add(users)
    db.commit()
    db.refresh(users)
    return  users 

@router.get("/{id}",response_model= schema.User)  
def get_user(id: int, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM "users" WHERE id = %s """, (str(id),))
    #user = cursor.fetchone()
    user = db.query(models.User_data).filter(models.User_data.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} was not found.")
    if user.owner_id != current_user.id:
     raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform this action")
     
        
    return user  


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_user(id : int,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM "users" WHERE id = %s returning *""",(str(id),))
    #delete_user = cursor.fetchone()
    #conn.commit()
    deleted_user_query = db.query(models.User_data).filter(models.User_data.id == id)
    deleted_user = deleted_user_query.first()

    
    if deleted_user == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User with id:{id} does not exist")
    if deleted_user.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform this action")
    deleted_user_query.delete(synchronize_session= False)
    db.commit() 
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model= schema.User)
def Update_User(id : int, updated_post : schema.UserCreate,db: Session = Depends(get_db),
current_user : int = Depends(oauth2.get_current_user) ):

    #cursor.execute("""UPDATE "users" SET name =%s, email=%s WHERE id=%s RETURNING *""",(post.Name, post.Email, str(id)))
    #updated_user = cursor.fetchone()
    #conn.commit()
    
    user_query = db.query(models.User_data).filter(models.User_data.id == id)

    post = user_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"User with id:{id} does not exist")
    user_query.update(updated_post.dict(), synchronize_session= False)
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized to perform this action")
    
    db.commit()
    return user_query.first() 

