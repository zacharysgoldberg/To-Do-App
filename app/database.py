from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


# connect_args={"check_same_thread": False} [for Sqlite only]
# engine = create_engine(os.getenv('DEV_DB'))
engine = create_engine(os.getenv('DATABASE_URI'))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
