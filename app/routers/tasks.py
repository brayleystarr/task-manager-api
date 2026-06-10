from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from app.db.database import SessionLocal 
from app.orm_models.orm_models import Task 
from app.pydantic_schemas.pydantic_schemas import TaskResponse, TaskCreate, TaskUpdate
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

# NOTE: CRUD operations defined below
# declare task creation endpoint 
@router.post('/tasks', status_code = status.HTTP_201_CREATED)
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

    '''
    although databse has been updated, 
    we return the json representation 
    of the new task to update the UI, 
    it now seeing fields of the new task
    that are handled by the database. this 
    allows us to avoide unecessary database querying
    '''
    return new_task

# declare task(s) reading endpoint
# NOTE : 
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

# declare task updating endpoint 
@router.patch('/tasks/{task_id}', response_model = TaskResponse)
def update_task(task_id : int, task_update : TaskUpdate, db : Session = Depends(get_db)):
    # fetch the task to update 
    task = db.query(Task).filter(Task.id ==  task_id).first()

    # handle missing tasks 
    if not task: 
        raise HTTPException(status_code = 404, detail = f"Task {task_id} not found")
    
    # cast update request -> dictionary 
    update_data = task_update.model_dump(exclude_unset = True)

    # apply updates 
    for key, value in update_data.items():
        setattr(task, key, value)

    # save changes to database 
    db.commit()

    # refresh object from database 
    db.refresh(task)

    # return the updated task (FastAPI converts via response_model)
    return task 

@router.delete('/tasks/{task_id}')
def delete_task(task_id : int, db : Session = Depends(get_db)):
    # fetch task to delete 
    task = db.query(Task).filter(Task.id == task_id).first()

    # client wishes to delete unexisting task 
    if not task: 
        raise HTTPException(status_code = 404, detail = f"Task {task_id} not found")
    
    # delete the task 
    db.delete(task)

    # commit the change 
    db.commit()

    # confirm task removal 
    return {"message" : f"Task {task_id} deleted successfully"}




    

    




