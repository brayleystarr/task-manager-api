from fastapi import APIRouter, Depends
from sqlalchemy.orm import session 
from app.db.database import SessionLocal 
from app.models.models import Task 

# init new router
router = APIRouter()

# maps requests to distinct db session 
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()