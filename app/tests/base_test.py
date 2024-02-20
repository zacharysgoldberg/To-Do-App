from unittest import TestCase
from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database import Base, get_db
from main import app
from fastapi.testclient import TestClient


"""
BaseTest

The parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

# ['Receipt' seed data]
merchant_name = "Test"
total = 14.50
tax = 2.50
merchant_address = '123 Address, City State Zip'
items_services = {
    "test_item_service": [
        {
            "description": "Description of items /or services",
            "quantity": 2,
            "price_per_item": 5.25
        },
        {
            "description": "Another description of items /or services",
            "quantity": 1,
            "price_per_item": 2.00
        }
    ]
}
transaction_number = "1234567891011"
card_last_4 = '1234'
link = 'link'
date = datetime.today().strftime("%Y-%m-%d")
time = datetime.now().strftime("%H:%M")

# ['Total' seed data]
totals = 10.50
tax_totals = 1.50
tax_year = '2022'


# def override_get_db():
#         try:
#             db = TestingSessionLocal()
#             yield db
#         finally:
#             db.close()


# app.dependency_overrides[get_db] = override_get_db

class BaseTest(TestCase):
    engine = create_engine("postgresql://postgres@localhost:5433/test-db")

    TestSession = sessionmaker(autocommit=False, bind=engine)

    @classmethod
    def setUp(self):
        # [Make sure test database exists]
        Base.metadata.create_all(bind=self.engine)

        # [Get test client]
        self.client = TestClient(app)

    def tearDown(self):
        # [Make sure test database is blank]
        Base.metadata.drop_all(bind=self.engine)


def _get_cookie_from_response(response, cookie_name):
    cookie_headers = response.headers.getlist("Set-Cookie")
    for header in cookie_headers:
        attributes = header.split(";")
        if cookie_name in attributes[0]:
            cookie = {}
            for attr in attributes:
                split = attr.split("=")
                cookie[split[0].strip().lower()] = split[1] if len(
                    split) > 1 else True
            return cookie
    return None
