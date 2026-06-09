from datetime import datetime 
from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

# declare ORM model defining database schema
class Task(Base):
    __tablename__ = "tasks"
    
    # NOTE: SQL will automatically increment the id 
    id = Column(Integer, primary_key=True, nullable=False) 
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(DateTime,  default=datetime.utcnow, nullable=True)
    priority = Column(String, nullable=True)


