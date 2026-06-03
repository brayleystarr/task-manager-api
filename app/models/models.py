from datetime import datetime 
from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

