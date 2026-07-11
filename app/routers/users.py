from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 

from app.db.database import SessionLocal 
from app.models.models import User
from app.schemas.pydantic_schemas import UserCreate, UserResponse, Token, UserLogin, TokenVerify
from app.routers.tasks import get_db
from app.auth.auth import hash_password, verify_password, get_current_user, create_access_token


# init container for route definitions
router = APIRouter()


@router.post('/users', status_code = status.HTTP_201_CREATED)
def create_user(user : UserCreate, db : Session = Depends(get_db)):
    """
    User Registration CRUD endpoint. 
    """

    new_user = User(
        email = user.email, 
        hashed_password = hash_password(user.password)
    )

    # has user already been registered?
    existing_user = db.query(User).filter(User.email == new_user.email).first() 
    if existing_user: 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = f"Email {user.email} has already been registered!"
        )

    # push new user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    
@router.post('/sessions') #, response_model = Token)
def login_user(user : UserLogin, db : Session = Depends(get_db)):
    """
    User login endpoint.
    """

    # fetch user 
    db_user = db.query(User).filter(User.email == user.email).first()  

    # user not found
    if not db_user: 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = "Invalid login attempt"
        )
    
    # correct password?
    if not verify_password(user.password, db_user.hashed_password): 
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Could not validate credentials", 
            headers = {"WWW-Authenticate" : "Bearer"}
        )

    # give JWT to user
    token = create_access_token({"user_id" : db_user.user_id })
    return {"token" : token}


@router.get('/me')
def verify_token(current_user: dict = Depends(get_current_user)):
    return {"valid_token": True}




    