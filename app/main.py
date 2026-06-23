from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.db.database import Base, engine 
from app.orm_models import orm_models
from app.routers.tasks import router as tasks_router
from app.routers.users import router as users_router
from dotenv import load_dotenv

# fetch environment variables
load_dotenv()

# init task-manager app
app = FastAPI()

# serve directory of frontend files 
app.mount("/static", StaticFiles(directory = "frontend"), name = "static")

# include tasks router CRUD functionality 
app.include_router(tasks_router)

# include user router CRUD functionality
app.include_router(users_router)

# bind ORM class to engine
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    """
    root endpoint, direct to user creation page
    """
    return FileResponse("frontend/create_user.html")
