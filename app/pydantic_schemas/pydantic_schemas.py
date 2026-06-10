from pydantic import BaseModel
from datetime import datetime

# task creation Pydantic model
class TaskCreate(BaseModel):
    title : str 
    description : str | None = None
    due_date : datetime | None = None
    priority : str | None = None

# task read Pydantic model 
class TaskResponse(BaseModel):
    id : int 
    title : str 
    description : str | None
    completed : bool 
    created_at : datetime
    due_date : datetime | None 
    priority : str | None 

# task update Pydantic model  
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    due_date: datetime | None = None
    priority: str | None = None

# user creation Pydantic model 
class UserCreate(BaseModel):
    email : str
    password : str