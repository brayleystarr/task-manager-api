import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
# --------------------------------------------------------
# NOTE: move this to the top of main.py after JWT is done ! 
#       ( this simply allows our code to read into our .env file )
from dotenv import load_dotenv
load_dotenv()
# --------------------------------------------------------

# import environment variables 
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# employ JWT init'n
def create_access_token(data : dict) -> str: 
    to_encode = data.copy()

    # set expiration time 
    expire_time = datetime.utcnow() + timedelta(
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # append expiration time to JWT payload 
    to_encode.update({"exp" : expire_time})

    # sign the token 
    encoded_jwt = jwt.encode(
        to_encode, 
        SECRET_KEY, 
        algorithm=ALGORITHM
    )

    return encoded_jwt

# decode given JWT
def verify_access_token(token : str):
    try: # attempt to decode JWT payload
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError: # invalid JWT input (malicious?)
        return None