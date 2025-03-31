from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import pathlib

# Load environment variables
load_dotenv()

# Get the current directory
BASE_DIR = pathlib.Path(__file__).parent.parent.parent.absolute()

# Check if we're running in Docker (data directory exists)
DATA_DIR = os.path.join(BASE_DIR, "data")
if os.path.exists(DATA_DIR):
    # Use the data directory for SQLite database in Docker
    SQLITE_DB_FILE = os.path.join(DATA_DIR, "review_analysis.db")
else:
    # Use the base directory for SQLite database in local development
    SQLITE_DB_FILE = os.path.join(BASE_DIR, "review_analysis.db")

# Create SQLite database URL
DATABASE_URL = f"sqlite:///{SQLITE_DB_FILE}"

# Create SQLAlchemy engine with SQLite
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
