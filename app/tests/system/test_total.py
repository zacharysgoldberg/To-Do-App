import os
from models import Total, User
from ..base_test import BaseTest


class TotalTest(BaseTest):
    def test_create_total(self):
        self.client.post('/auth/register', data={
            'username': os.getenv('MAIL_USERNAME'),
            'email': os.getenv('MAIL_USERNAME'),
            'email2': os.getenv('MAIL_USERNAME'),
            'password': os.getenv('PASSWORD'),
            'confirm_password': os.getenv('PASSWORD'),
        })
        response = self.client.post('/')

    def test_create_duplicate_total(self):
        pass

    def test_delete_total(self):
        pass

    def test_find_total(self):
        pass

    def test_total_not_found(self):
        pass

    def test_total_found_with_receipts(self):
        pass

    def test_total_list(self):
        pass

    def test_total_list_with_receipts(self):
        pass
