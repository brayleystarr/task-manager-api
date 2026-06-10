from fastapi.testclient import TestClient
from app.main import app 
from app.db.database import SessionLocal
from app.orm_models.orm_models import Task
import pytest

'''
NOTE: FastAPI automatically provides a way for us to test our API like a real client 
      without running a server. You test your app through HTTP calls - just like 
      a browser and frontend would. We can test the correctness of our CRUD operations through using the TestClient provided by 
      FastAPI. We simulate said client making different HTTP requests WITHOUT an actual server running 
      in the background. Once said TestClient makes the HTTP request, FastAPI will return a TestResponse 
      object, containing attributes, there being a status code, a Json body, and (rarely) a raw text.
'''

client = TestClient(app)

# use pytest fixture to streamline database communication sessions 
@pytest.fixture
def db(): 
    db = SessionLocal()
    try: 
        yield db 
    finally: 
        db.close()

'''
NOTE: Testing our task creation CRUD operation: 
    (i) returns correct json?
    (ii) returns correct status code?
    (iii) updates database with new task?
'''

@pytest.mark.parametrize("task_data", [
    {
        "title": "Task1",
        "description": None,
        "due_date": None,
        "priority": None
    },
    {
        "title": "Task2",
        "description": "desc",
        "due_date": None,
        "priority": "low"
    },
    {
        "title": "Task3",
        "description": "desc3",
        "due_date": "2026-06-10T00:00:00",
        "priority": "high"
    },
])

def test_create_task(task_data, db):
    # simulate client using app W/O server
    response = client.post("/tasks", json = task_data)

    # correct status code?
    assert response.status_code == 201

    # correct attributes in json output?
    response_data = response.json()
    assert response_data["id"] is not None
    assert response_data["title"] == task_data["title"]
    assert response_data["description"] == task_data["description"]
    assert response_data["completed"] is False
    assert response_data["created_at"] is not None
    assert (response_data["due_date"] is None) or (response_data["due_date"] == task_data["due_date"])
    assert response_data["priority"] == task_data["priority"]   

    # correctly pushed onto database?
    task = db.query(Task).filter(Task.id == response_data["id"]).first() 
    assert task is not None
    assert task.title == task_data["title"]
                
                           
                           
    