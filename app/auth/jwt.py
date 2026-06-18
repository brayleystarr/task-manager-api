import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# --------------------------------------------------------
# NOTE: move this to the top of main.py after JWT is done ! 
#       ( this simply allows our code to read into our .env file )
from dotenv import load_dotenv
load_dotenv()
# --------------------------------------------------------

# import environment-variables 
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data : dict) -> str: 
    """
    take user data and turn it inot a signed (encrypted), time-limited 
    token string that can be safely sent to clients and later verified
    """

    # NOTE: this is the JWT payload! this will contain 
    #       the user's user_id, so we can remember them 
    #       (since HTTP(s) is a 'stateless' protocol)
    to_encode = data.copy()

    # how long should the JWT be valid for?
    expire_time = datetime.utcnow() + timedelta(
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # append expiration time to JWT payload 
    to_encode.update({"exp" : expire_time})

    # init JWT with signed token string for verification 
    encoded_jwt = jwt.encode(
        to_encode,  # JWT payload
        SECRET_KEY,  # secret key for signing, and...  
        algorithm = ALGORITHM # how to sign it 
    )

    # output the jwt with the signed token string 
    return encoded_jwt


def verify_access_token(token : str):
    """
    given JWT header, payload, and signature, recompute 
    signature using secret key, compare computer signature 
    against given signature to check for maliciousness
    """
    try: # valid signature?
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError: # JWT (probably) has invalid signature 
        return None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")


def get_current_user(token: str = Depends(oauth2_scheme)): 
    """
    get user_id from JWT payload.  

    NOTE: the 'Depends' function will: 
            1. look at the incoming HTTP request 
            2. read the Authorization header 
            3. extract the JWT 
            4. pass the JWT into the token argument
    """

    # exception to raise in the case of invalid JWT signature
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED, 
        detail = "Could not validate credentials", 
        headers = {"WWW-Authenticate" : "Bearer"}
    )    

    try: 
        # fetch payload from JWT, after we verify signature
        payload = verify_access_token(token)

        if payload is None: # invalid signature, or other JWT error
            raise credentials_exception

        # fetch user identity from JWT payload 
        user_id = payload.get("user_id")

        # user identity not found in JWT payload
        if user_id is None: 
            raise credentials_exception 
        
    except JWTError: # something wrong with token during decoding/verification 
        raise credentials_exception

    # produce user_id taken from the JWT payload
    return user_id

        

    
