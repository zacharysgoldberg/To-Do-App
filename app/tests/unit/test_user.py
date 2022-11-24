from .unit_base_test import UnitBaseTest
from models import User


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = User('email@domain.com',
                    'password',
                    'username')

        self.assertEqual(user.email, 'email@domain.com')
        self.assertEqual(user.password, 'password')
        self.assertEqual(user.username, 'username')
