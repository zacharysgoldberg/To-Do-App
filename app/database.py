from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres@localhost:5432/to-do-app"
SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:5432/{os.getenv('DATABASE_NAME')}?sslmode=require"

# connect_args={"check_same_thread": False} [for Sqlite only]
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
