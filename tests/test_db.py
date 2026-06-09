from app.db.database import SessionLocal 
from app.orm_models.orm_models import Task

# NOTE: anytime you want to interact with your database, 
#       you create a new session using the function SessionLocal()

# init new session
db = SessionLocal()

# declare new task object
new_task = Task(
    title = "Test task", 
    description="this is my frist DB insert", 
    completed=False
)

# push new task to database
db.add(new_task)
db.commit()
db.refresh(new_task)
print("Created task:", new_task.id, new_task.title)
db.close()

