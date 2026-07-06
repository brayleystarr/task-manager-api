import os 
from datetime import datetime, timedelta 

from dotenv import load_dotenv 
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext 


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto") # encryption algo for passwords
ALGORITHM = os.getenv("ALGORITHM") # encryption algo for JWTs 

def hash_password(password : str) -> str:
    """Hash a plaintext password using brcypt.""" 
    return PWD_CONTEXT.hash(password)


def verify_password(plain_password : str, hashed_password : str) -> str:
    """Compare plaintext password's hash against existing hash string."""
    return PWD_CONTEXT.verify(plain_password, hashed_password)





