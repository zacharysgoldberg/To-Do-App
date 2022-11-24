import os
import simplejson as json
from datetime import datetime
from models import Receipt, User, Total
from ..base_test import (BaseTest, merchant_name, total,
                         tax, address, items_services, transaction_number,
                         card_last_4, link, date, time)
from database import load


class ReceiptTest(BaseTest):
    def test_crud(self):
        with self.TestSession() as db:
            user = User(os.getenv('MAIL_USERNAME'),
                        os.getenv('MAIL_USERNAME'),
                        os.getenv('PASSWORD'))

            db.add(user)
            db.commit()

            total_model = Total(total, tax, date[0:4], user.id)

            db.add(total_model)
            db.commit()

            receipt = Receipt(merchant_name, total, tax, address, items_services, transaction_number,
                              card_last_4, link, date, datetime.strptime(time, '%H:%M'), total_model.id, user.id)

            db.add(receipt)
            db.commit()
            # [ensure receipt object is not none]
            self.assertIsNotNone(db.query(
                Receipt).filter(Receipt.id == receipt.id))

        # [remove user, total, and receipt objects from db]
        # db.delete(receipt)
        # db.delete(total)
        # db.delete(user)
        # # db.commit()
        # # [ensure user, total, and receipt objects are removed from db]
        # self.assertIsNone(Receipt.query.get(receipt.id))
        # self.assertIsNone(Total.query.get(total_model.id))
        # self.assertIsNone(User.query.get(1))

    def test_total_relationship(self):
        with self.TestSession() as db:
            user = User(username=os.getenv('MAIL_USERNAME'),
                        email=os.getenv('MAIL_USERNAME'),
                        password=os.getenv('PASSWORD'))

            db.add(user)
            db.commit()

            total_model = Total(total, tax, date[0:4], user.id)

            db.add(total_model)
            db.commit()

            receipt = Receipt(merchant_name, total, tax, address, items_services,
                              transaction_number, card_last_4, link,
                              date, datetime.strptime(time, '%H:%M'), total_model.id, user.id)

            db.add(receipt)
            db.commit()
            # [ensure receipt FK id equals total id]
            self.assertEqual(receipt.total_id, total_model.id)

    def test_receipt_json(self):
        self.maxDiff = None
        with self.TestSession() as db:
            user = User(username=os.getenv('MAIL_USERNAME'),
                        email=os.getenv('MAIL_USERNAME'),
                        password=os.getenv('PASSWORD'))

            db.add(user)
            db.commit()

            total_model = Total(total, tax, date[0:4], user.id)

            db.add(total_model)
            db.commit()

            receipt = Receipt(
                merchant_name, total, tax, address, items_services,
                transaction_number, card_last_4, link,
                date, datetime.strptime(time, '%H:%M'), total_model.id, user.id
            )

            db.add(receipt)
            db.commit()

            expected = {
                'id': receipt.id,
                'merchant_name': merchant_name,
                'total': json.dumps(total, use_decimal=True),
                'tax': json.dumps(tax, use_decimal=True),
                'merchant_address': address,
                'items_services': items_services,
                'transaction_number': transaction_number,
                'card_last_4': card_last_4,
                'link': link,
                'date': json.dumps(date, indent=4, sort_keys=True),
                'time': json.dumps(datetime.strptime(time, '%H:%M'), indent=4, sort_keys=True, default=str),
                'total_id': total_model.id,
                'user_id': user.id
            }

        self.assertDictEqual(receipt.serialize(), expected)
