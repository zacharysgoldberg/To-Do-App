from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


# EB_DATABASE_URI = os.getenv('DATABASE_URI')
DEV_DB = os.getenv('DEV_DB')
# connect_args={"check_same_thread": False} [for Sqlite only]
engine = create_engine(DEV_DB)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
