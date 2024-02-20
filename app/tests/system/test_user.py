import json
import os
from models import User
from ..base_test import BaseTest, _get_cookie_from_response
import httpx

# from parameterized import parameterized_class


class UserTest(BaseTest):
    def test_register_user(self):
        response = self.client.post('/auth/register', data={
            'username': os.getenv('MAIL_USERNAME'),
            'email': os.getenv('MAIL_USERNAME'),
            'email2': os.getenv('MAIL_USERNAME'),
            'password': os.getenv('PASSWORD'),
            'confirm_password': os.getenv('PASSWORD'),
        })

        self.assertEqual(response.status_code, 200)

        with self.TestSession.begin() as db:
            self.assertIsNotNone(
                db.query(User).filter(
                    User.email == os.getenv('MAIL_USERNAME'))
            )

    def test_register_and_login(self):
        self.client.post('/auth/register', data={
            'username': os.getenv('MAIL_USERNAME'),
            'email': os.getenv('MAIL_USERNAME'),
            'email2': os.getenv('MAIL_USERNAME'),
            'password': os.getenv('PASSWORD'),
            'confirm_password': os.getenv('PASSWORD'),
        })

        response = self.client.post(
            '/auth/token', data={'username': os.getenv('MAIL_USERNAME'), 'password': os.getenv('PASSWORD')}
        )

        self.assertEqual(response.status_code, 200)

        # cookies = response.headers.getlist('Set-Cookie')
        # self.assertEqual(len(cookies), 4)

        # access_cookie = _get_cookie_from_response(
        #     response, "access_token_cookie")
        # self.assertIsNotNone(access_cookie)

        # access_csrf_cookie = _get_cookie_from_response(
        #     response, 'csrf_access_token')
        # self.assertIsNotNone(access_csrf_cookie)

    def test_register_duplicate_user(self):
        self.client.post('/auth/register', data={
            'username': os.getenv('MAIL_USERNAME'),
            'email': os.getenv('MAIL_USERNAME'),
            'email2': os.getenv('MAIL_USERNAME'),
            'password': os.getenv('PASSWORD'),
            'confirm_password': os.getenv('PASSWORD'),
        })
        response = self.client.post('/auth/register', data={
            'username': os.getenv('MAIL_USERNAME'),
            'email': os.getenv('MAIL_USERNAME'),
            'email2': os.getenv('MAIL_USERNAME'),
            'password': os.getenv('PASSWORD'),
            'confirm_password': os.getenv('PASSWORD'),
        })

        self.assertIn("Email or Username is already in use", response.text)
