from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from app.db.database import SessionLocal 
from app.models.models import Task 
from app.schemas.task import TaskResponse, TaskCreate
from typing import List

# init container for route definitions
router = APIRouter()

# maps requests to distinct db session 
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

# NOTE : CRUD operations defined below

# declare task creation endpoint 
@router.post('/tasks')
def create_task(task : TaskCreate, db : Session = Depends(get_db)):  
    # convert Pydantic -> ORM 
    new_task = Task(
        title = task.title,
        description = task.description,
        completed = False,
        due_date = task.due_date,
        priority = task.priority
    )
    # push new task to database
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# declare task(s) reading endpoint
@router.get('/tasks', response_model = List[TaskResponse])
def get_tasks(db : Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# declare task reading endpoint 
@router.get('/tasks', response_model = TaskResponse)
def get_task(task_id : int, db : Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    # invalid task id 
    if not task: 
        raise HTTPException(status_code = 404, detail = f"Task {task_id} not found")
    # output valid task id 
    return task 




