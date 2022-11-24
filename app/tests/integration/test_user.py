import os
from ..base_test import BaseTest
from models import User


class UserTest(BaseTest):
    def test_crud(self):
        with self.TestSession() as db:
            user = User(username=os.getenv('MAIL_USERNAME'),
                        email=os.getenv('MAIL_USERNAME'),
                        password=os.getenv('MAIL_PASSWORD'))
            db.add(user)

        self.assertIsNotNone(db.query(User).filter(
            User.username == user.username))
