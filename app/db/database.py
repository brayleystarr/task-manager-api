from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# declare connective string
DATABASE_URL = "postgresql+psycopg2://taskuser:password@localhost:5432/taskdb"

# init engine 
engine = create_engine(DATABASE_URL)

# init session object factory
SessionLocal = sessionmaker(
    bind=engine, 
    autoflush=False, 
    autocommit=False
)

# init registry for all model metadata for table creation 
Base = declarative_base()






