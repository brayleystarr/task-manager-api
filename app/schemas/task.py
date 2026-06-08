from pydantic import BaseModel
from datetime import datetime

# task create pydantic model
class TaskCreate(BaseModel):
    title : str 
    desription : str | None = None
    due_date : datetime | None = None
    priority : str | None = None

# task read pydantic model 
class TaskResponse(BaseModel):
    id : int 
    title : str 
    desription : str | None
    completed : bool 
    created_at : datetime
    due_date : datetime | None 
    priority : str | None 

# task update pydantic model  
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    due_date: datetime | None = None
    priority: str | None = None
