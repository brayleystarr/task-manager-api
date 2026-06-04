from fastapi import FastAPI
from app.db.database import Base, engine 
from app.models import models

# NOTE: to init the database: 
# 1. CREATE DATABASE taskdb (done one time only!)
# 2. connect engine to taskdb (using connective string)
# 3. define database schema(s)
# 4. create_all() (converts models -> SQL)
# 5. PostgreSQL executes CREATE TABLE statements

# init task-manager application
app = FastAPI()

# bind ORM schemas to engine
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message" : "Hello World!"}

