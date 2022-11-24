import simplejson as json
from models import Receipt
from .unit_base_test import UnitBaseTest, error_message
from datetime import datetime

date = datetime.today().strftime("%Y-%m-%d")
time = datetime.now().strftime("%H:%M")

receipt = Receipt('merchant_name', 5.00, 0.50, 'address', {},
                  '1234567891011', '1234', 'link', date, time, 1, 1)

# [testing receipt model]


class ReceiptTest(UnitBaseTest):
    def test_create_receipt(self):
        self.assertEqual('merchant_name', receipt.merchant_name,
                         error_message('from'))
        self.assertEqual(5.00, receipt.total,
                         error_message('total'))
        self.assertEqual(0.50, receipt.tax, error_message('tax'))
        self.assertEqual('address', receipt.merchant_address,
                         error_message('address'))
        self.assertDictEqual({}, receipt.items_services,
                             error_message('items_services'))
        self.assertEqual('1234567891011',
                         receipt.transaction_number, error_message('transaction_number'))
        self.assertEqual('1234', receipt.card_last_4,
                         error_message('card_last_4'))
        self.assertEqual('link', receipt.link, error_message('link'))
        self.assertEqual(date, receipt.date,
                         error_message('date'))
        self.assertEqual(time, receipt.time, error_message('time'))
        self.assertEqual(1, receipt.total_id, error_message('total_id'))
        self.assertEqual(1, receipt.user_id, error_message('user_id'))

    def test_serializer_no_receipts(self):
        self.maxDiff = None
        expected = {
            'id': None,
            'merchant_name': 'merchant_name',
            'total': json.dumps(5.00, use_decimal=True),
            'tax': json.dumps(0.50, use_decimal=True),
            'merchant_address': 'address',
            'items_services': {},
            'transaction_number': '1234567891011',
            'card_last_4': '1234',
            'link': 'link',
            'date': json.dumps(date, indent=4, sort_keys=True, default=str),
            'time': json.dumps(time, indent=4, sort_keys=True, default=str),
            'total_id': 1,
            'user_id': 1
        }

        self.assertEqual(expected, receipt.serialize(),
                         f"The JSON export of the receipt is incorrect. Received {receipt.serialize()}, expected {expected}")
