import os 
from datetime import datetime, timedelta 

from dotenv import load_dotenv 
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext 


load_dotenv()

# NOTE: this allows us to fetch the JWT from the HTTP header
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl = "login")
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


def create_access_token(user_data : dict) -> str: 
    """ Create a JWT for a user."""
    to_encode = user_data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire_time})

    # init JWT
    encoded_jwt = jwt.encode(
        to_encode,  
        SECRET_KEY,  
        algorithm = ALGORITHM)

    return encoded_jwt        


def get_current_user(token: str = Depends(OAUTH2_SCHEME)): 
    """
    Identify a specific user from a JWT.
    """

    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED, 
        detail = "Could not validate credentials", 
        headers = {"WWW-Authenticate" : "Bearer"})    

    try: 
        payload = jwt.decode( 
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM])

        user_id = payload.get("user_id")

        if user_id is None or not isinstance(user_id, int): 
            raise credentials_exception 
        
    except JWTError: # invalid JWT 
        raise credentials_exception

    return user_id






