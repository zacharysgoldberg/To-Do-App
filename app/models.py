from sqlalchemy import Boolean, Column, Integer, Date, String, ForeignKey, Numeric, DateTime
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    reset_token = Column(String, nullable=True)

    receipts = relationship('Receipt', cascade="all, delete",
                            backref='users')
    totals = relationship('Total', cascade='all, delete',
                          backref='users')


class Total(Base):
    __tablename__ = 'totals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    purchase_totals = Column(Numeric, nullable=False)
    tax_totals = Column(Numeric, nullable=False)
    tax_year = Column(String, nullable=False, index=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receipts = relationship(
        "Receipt", backref="totals", lazy='dynamic')


class Receipt(Base):
    __tablename__ = 'receipts'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    _from = Column(String, nullable=False)
    purchase_total = Column(String, nullable=False)
    tax = Column(Numeric, nullable=False)
    address = Column(String, nullable=False)
    items_services = Column(JSON, nullable=False)
    transaction_number = Column(String, nullable=True, unique=True)
    cash = Column(Boolean, nullable=True)
    card_last_4 = Column(String(4), nullable=True)
    link = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    time = Column(DateTime, nullable=True)

    total_id = Column(Integer, ForeignKey('totals.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
