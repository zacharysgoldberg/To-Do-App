import os
import json
from models import User
from ..base_test import BaseTest, _get_cookie_from_response, get_db
from utils.receipt_ocr import receipt_ocr
from utils.existing_year import existing_year


# TODO: Receipt System Test


class TestReceipt(BaseTest):
    def test_create_receipt(self):
        self.maxDiff = None
        with self.TestSession.begin() as db:
            self.client.post('/auth/register', data={
                'username': os.getenv('MAIL_USERNAME'),
                'email': os.getenv('MAIL_USERNAME'),
                'email2': os.getenv('MAIL_USERNAME'),
                'password': os.getenv('PASSWORD'),
                'confirm_password': os.getenv('PASSWORD'),
            })

            response = self.client.post('/auth/token', data={
                'email': os.getenv('MAIL_USERNAME'),
                'password': os.getenv('PASSWORD')
            })

            # windows_file = "C:/Users/Goldb/OneDrive/Desktop/receipt-manager/app/api/receipts/test_receipt.pdf"
            # linux_file = "/mnt/c/Users/Goldb/OneDrive/Desktop/receipt-manager/app/api/receipts/test_receipt.pdf"
            file = "src/images/test_receipt.pdf"
            # receipt = receipt_ocr(file)

            # existing_year(receipt[0], 1, receipt[0]['date'][0:4], db)

            # csrf_token = _get_cookie_from_response(
            #     response, "csrf_access_token")['csrf_access_token']
            # headers = {"X-CSRF-TOKEN-ACCESS": csrf_token}

            # response = self.client.get(
            #     '/receipts', headers=headers)

            # print(response)

            # self.assertEqual(response.status_code, 200)
            # self.assertDictEqual(receipt[0], response.json)

    def test_delete_receipt(self):
        pass

    def test_find_receipt(self):
        pass

    def test_receipt_not_found(self):
        pass

    def test_total_found_with_receipt(self):
        pass

    def test_get_all_receipts(self):
        pass
