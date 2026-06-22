from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from app.db.database import SessionLocal 
from app.orm_models.orm_models import User
from app.pydantic_schemas.pydantic_schemas import UserCreate, UserResponse, Token, UserLogin
from app.routers.tasks import get_db
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import create_access_token

# init container for route definitions
router = APIRouter()

# NOTE: user CRUD operations defined below
@router.post('/users', status_code = status.HTTP_201_CREATED, response_model = UserResponse)
def create_user(user : UserCreate, db : Session = Depends(get_db)):
    """
    user registration endpoint
    """

    # convert Pydantic model -> ORM model 
    new_user = User(
        email = user.email, 
        password = hash_password(user.password)
    )

    # has this user already made an account?
    existing_user = db.query(User).filter(User.email == new_user.email).first()

    # raise exception when registering existing user    
    if existing_user: 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = f"Email {user.email} already registered"
        )

    # push new task to database 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # return JSON response
    return new_user

@router.post('/login', response_model = Token)
def login_user(user : UserLogin, db : Session = Depends(get_db)):

    # fetch user from databse
    db_user = db.query(User).filter(User.email == user.email).first()

    # user not found
    if not db_user: 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail = "Invalid login attempt"
        )
    
    # verify correct password 
    if not verify_password(user.password, db_user.password): 
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Could not validate credentials", 
            headers = {"WWW-Authenticate" : "Bearer"}
        )

    # create JWT for user 
    access_token = create_access_token({"user_id" : db_user.id})

    # return JWT 
    return {
        "access_token" : access_token, 
        "token_type" : "bearer"
    }