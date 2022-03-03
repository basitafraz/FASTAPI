import secrets
from fastapi import FastAPI
from .routers import user_input, user_output, auth
from random import randrange
from . import models
from .database import engine 
from .config import settings



models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

app.include_router(user_input.router)
app.include_router(user_output.router)
app.include_router(auth.router) 





