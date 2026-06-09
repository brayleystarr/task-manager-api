from fastapi.testclient import TestClient
from app.main import app 
import pytest

# NOTE: FastAPI automatically provides a way for us to test our API like a real client 
#       without running a server. You test your app through HTTP calls - just like 
#       a browser and frontend would 
client = TestClient(app)

# NOTE: We can test the correctness of our CRUD operations through using the TestClient provided by 
#       FastAPI. We simulate said client making different HTTP requests WITHOUT an actual server running 
#       in the background. Once said TestClient makes the HTTP request, FastAPI will return a TestResponse 
#       object, containing attributes, there being a status code, a Json body, and (rarely) a raw text. 

@pytest.mark.parametrize("task_data", [
    {"title" : "Task1", "priority" : "low"},
    {"title" : "Task2", "priority" : "high"}, 
    {"title" : "Task3", "priority" : None},
])        
def test_create_task(task_data):
    response = client.post("/tasks", json = task_data)

    assert response.status_code == 200
    assert response.json()["title"] == task_data["title"]



                           
                           
                           
                           
    