# This module is responsible for creating a database session using SQLAlchemy. 
# It defines the necessary configurations and establishes a connection to the database.
from sqlalchemy import create_engine
# The database URL is retrieved from the environment variable DATABASE_URL.
from sqlalchemy.orm import sessionmaker, declarative_base  


DATABASE_URL = "sqllite:///./storage/planthealth.db" # plant health image db URL

engine = create_engine(
    DATABASE_URL,  # URL 
    connect_args={"check_same_thread": False}  # SQLite specific argument
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # Base class for declarative models

def get_db():
    """
    Dependency function to get a database session.
    This function is used for FastAPI routes to provide a database session.
    """
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Yield the session to the caller
    finally:
        db.close()  # Ensure the session is closed after use