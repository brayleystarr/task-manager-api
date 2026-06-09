from app.db.database import engine, Base 

def reset_db():
    # clear database's contents
    Base.metadata.drop_all(bind=engine)

    # re-init database using ORM model 
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    reset_db()
    print("Database reset complete!")
