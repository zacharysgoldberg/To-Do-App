from sqlalchemy import Boolean, Column, Integer, Date, String, ForeignKey, Numeric, DateTime
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from database import Base
from sqlalchemy.orm import relationship
import simplejson as json


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

    #  [contructor for column types]
    def __init__(self, email: str, password: str, username: str):
        self.email = email
        self.password = password
        self.username = username

    # [serializer returned as a dict/json object]
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }


class Total(Base):
    __tablename__ = 'totals'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    totals = Column(Numeric, nullable=False)
    tax_totals = Column(Numeric, nullable=False)
    tax_year = Column(String, nullable=False, index=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receipts = relationship(
        "Receipt", backref="totals", lazy='dynamic')

    def __init__(self, totals: float, tax_totals: float, tax_year: str, user_id: int):
        self.totals = totals
        self.tax_totals = tax_totals
        self.tax_year = tax_year
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            # [Hack to serialize decimal values into JSON]
            'totals': json.dumps(self.totals, use_decimal=True),
            'tax_totals': json.dumps(self.tax_totals, use_decimal=True),
            # [declared year as int type rather than date]
            'tax_year': self.tax_year,
            'user_id': self.user_id
        }


class Receipt(Base):
    __tablename__ = 'receipts'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    merchant_name = Column(String, nullable=False)
    total = Column(Numeric, nullable=False)
    tax = Column(Numeric, nullable=False)
    merchant_address = Column(String, nullable=False)
    items_services = Column(JSON, nullable=False)
    transaction_number = Column(String, nullable=True)
    card_last_4 = Column(String(4), nullable=True)
    link = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    time = Column(DateTime, nullable=True)

    total_id = Column(Integer, ForeignKey('totals.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, merchant_name: str, total: float, tax: float, address: str,
                 items_services: dict, transaction_number: str, card_last_4: str,
                 link: str, date: str, time: str, total_id: int, user_id: int):
        self.merchant_name = merchant_name
        self.total = total
        self.tax = tax
        self.merchant_address = address
        self.items_services = items_services
        self.transaction_number = transaction_number
        self.card_last_4 = card_last_4
        self.link = link
        self.date = date
        self.time = time
        self.total_id = total_id
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'merchant_name': self.merchant_name,
            'total': json.dumps(self.total, use_decimal=True),
            'tax': json.dumps(self.tax, use_decimal=True),
            'merchant_address': self.merchant_address,
            'items_services': self.items_services,
            'transaction_number': self.transaction_number,
            'card_last_4': self.card_last_4,
            'link': self.link,
            'date': json.dumps(self.date, indent=4, sort_keys=True, default=str),
            'time': json.dumps(self.time, indent=4, sort_keys=True, default=str),
            'total_id': self.total_id,
            'user_id': self.user_id
        }
