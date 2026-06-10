from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from app.db.database import SessionLocal 
from app.orm_models.orm_models import User
from app.pydantic_schemas.pydantic_schemas import UserCreate
from app.routers.tasks import get_db
from app.auth.hashing import hash_password, verify_password

# init container for route definitions
router = APIRouter()

'''
# NOTE: user CRUD operations defined below
@router.post('/users', status_code = status.HTTP_201_CREATED)
def create_user(user : UserCreate, db : Session = Depends(get_db)):
    # convert Pydantic model -> ORM model 
    new_user = User(
        email = user.email, 
        password = hash_password(user.password)
    )

    # push new task to database 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
'''
