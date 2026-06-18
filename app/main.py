from fastapi import FastAPI
from app.db.database import Base, engine 
from app.orm_models import orm_models
from app.routers.tasks import router as tasks_router
from dotenv import load_dotenv

# allow access to environment variables
load_dotenv()

# NOTE: to init the database: 
# 1. CREATE DATABASE taskdb (done one time only!)
# 2. connect engine to taskdb (using connective string)
# 3. define database schema(s)
# 4. create_all() (converts models -> SQL)
# 5. PostgreSQL executes CREATE TABLE statements

# init task-manager application
app = FastAPI()

# include tasks router CRUD functionality 
app.include_router(tasks_router)

# bind ORM schemas to engine
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message" : "Hello World!"}

