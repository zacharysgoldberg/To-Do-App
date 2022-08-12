from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres@localhost:5432/todos"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres@db:5432/todos"

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
