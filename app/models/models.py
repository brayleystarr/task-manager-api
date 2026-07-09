from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from app.db.database import Base


# NOTE: the Task and User ORMs listed below define the framework of our database


class Task(Base):
    __tablename__ = "tasks"
 
    #id = Column(Integer, primary_key=True, nullable=False) # NOTE: I think this is overkill... user_id should be sufficient
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable = False)
    task_id = Column(Integer, primary_key=True, index=True,  nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    due_date = Column(DateTime,  default=datetime.now(timezone.utc), nullable=True)
    priority = Column(String, nullable=True) # TODO: change this to an enum type? should only be 
                                                #       either LOW, MEDIUM, or HIGH


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    


