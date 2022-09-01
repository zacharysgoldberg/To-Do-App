from sqlalchemy import Boolean, Column, Integer, Date, String, ForeignKey
from datetime import datetime
from database import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    reset_token = Column(String, nullable=True)

    todos = relationship('ToDos', cascade="all, delete",
                         back_populates='users')


class ToDos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Integer, nullable=False)
    complete = Column(Boolean, default=False, nullable=False)
    date = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    users = relationship('Users', back_populates='todos')
