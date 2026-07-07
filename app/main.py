from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.db.database import Base, engine 
from app.orm_models import orm_models
from app.routers.tasks import router as tasks_router
from app.routers.users import router as users_router
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# fetch environment variables
load_dotenv()

# init task-manager app
app = FastAPI()

# add CORSMiddleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# serve directory of frontend files 
app.mount("/static", StaticFiles(directory = "static"), name = "static")

# include tasks router CRUD functionality 
app.include_router(tasks_router)

# include user router CRUD functionality
app.include_router(users_router)

# bind ORM class to engine
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    """
    Root endpoint, redirects user to registration page
    """
    return RedirectResponse(url="/register")

@app.get("/register")
def register_page():
    """
    User registration page. 
    """
    return FileResponse("static/create_user.html")

# NOTE: DELETE LATER, this is to simply test the 
#       user login logic '
@app.get("/testing")
def testing_page():
    """
    User registration page. 
    """
    return FileResponse("static/test.html")
