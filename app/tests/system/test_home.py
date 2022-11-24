from ..base_test import BaseTest


class TestHome(BaseTest):
    def test_home(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
