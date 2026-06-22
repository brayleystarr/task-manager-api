from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from app.db.database import SessionLocal 
from app.orm_models.orm_models import Task 
from app.pydantic_schemas.pydantic_schemas import TaskResponse, TaskCreate, TaskUpdate
from typing import List
from app.auth.jwt import get_current_user

# init container for route definitions
router = APIRouter()

# maps HTTP requests to distinct db session 
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

# NOTE: CRUD operations defined below
 
@router.post('/tasks', status_code = status.HTTP_201_CREATED, response_model = TaskResponse)
def create_task(task : TaskCreate, db : Session = Depends(get_db), current_user_id : int = Depends(get_current_user)):  
    """
    task creation CRUD endpoint        
    """

    # Pydantic object -> ORM object instance 
    new_task = Task(
        user_id = current_user_id, 
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
    NOTE: although databse has been updated, 
          we return the json representation 
          of the new task to update the UI, 
          it now seeing fields of the new task
          that are handled by the database. this 
          allows us to avoide unecessary database querying
    '''
    return new_task


@router.get('/tasks', response_model = List[TaskResponse])
def get_tasks(db : Session = Depends(get_db), current_user_id : int = Depends(get_current_user)):
    """
    list all tasks associated with given user 
    """
    tasks = db.query(Task).filter(Task.user_id == current_user_id)
    return tasks

@router.get('/tasks', response_model = TaskResponse)
def get_task(task_id : int, db : Session = Depends(get_db), current_user_id : int = Depends(get_current_user)):
    """
    list specific task of specific user 
    """

    # fetch first instance of task with given user and task id 
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user_id).first()

    # task not found 
    if not task: 
        raise HTTPException(status_code = 404, detail = f"Task {task_id} not found")
    
    # output valid task id 
    return task 


@router.patch('/tasks/{task_id}', response_model = TaskResponse)
def update_task(task_id : int, task_update : TaskUpdate, db : Session = Depends(get_db), current_user_id = Depends(get_current_user)):
    """
    update given task under given user
    """

    # fetch the task to update 
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user_id).first()

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
def delete_task(task_id : int, db : Session = Depends(get_db), current_user_id = Depends(get_current_user)):
    """
    delete given task under given user
    """

    # fetch task to delete 
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user_id).first()

    # client wishes to delete unexisting task 
    if not task: 
        raise HTTPException(status_code = 404, detail = f"Task {task_id} not found")
    
    # delete the task 
    db.delete(task)

    # commit the change 
    db.commit()

    # confirm task removal 
    return {"message" : f"Task {task_id} deleted successfully"}




    

    




