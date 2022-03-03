from passlib.context import CryptContext

pwd_context = CryptContext(schemes= ["bcrypt"], deprecated = "auto") #we're telling passlib that we are using brypt as our default hashing algorithm.

def hash(password : str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)