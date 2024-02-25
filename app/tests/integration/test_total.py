import os
from datetime import datetime
import simplejson as json
from models import Total, User, Receipt
from ..base_test import (BaseTest, merchant_name, total, tax,
                         merchant_address, items_services, transaction_number,
                         card_last_4, link, date, time,
                         totals, tax_totals, tax_year)
from database import load


class TotalTest(BaseTest):
    def test_create_total(self):
        with self.TestSession() as db:
            user = User(username=os.getenv('MAIL_USERNAME'),
                        email=os.getenv('MAIL_USERNAME'),
                        password=os.getenv('PASSWORD'))
            db.add(user)
            db.commit()

            total_model = Total(totals, tax_totals, tax_year, user.id)

            db.add(total_model)
            db.commit()

        self.assertListEqual(total_model.receipts.all(), [])

    def test_crud(self):
        with self.TestSession() as db:
            user = User(username=os.getenv('MAIL_USERNAME'),
                        email=os.getenv('MAIL_USERNAME'),
                        password=os.getenv('PASSWORD'))
            db.add(user)
            db.commit()

            total_model = Total(
                totals, tax_totals, tax_year, user.id)

            db.add(total_model)
            db.commit()

            self.assertIsNotNone(db.query(Total).filter(
                Total.id == user.id))

    def test_total_relationship(self):
        with self.TestSession() as db:
            user = User(username=os.getenv('MAIL_USERNAME'),
                        email=os.getenv('MAIL_USERNAME'),
                        password=os.getenv('PASSWORD'))

            db.add(user)
            db.commit()

            total_model = Total(totals, tax_totals, tax_year, user.id)

            db.add(total_model)
            db.commit()

            receipt = Receipt(
                merchant_name, total, tax, merchant_address, items_services,
                transaction_number, card_last_4, link,
                date, datetime.strptime(time, '%H:%M'), total_model.id, user.id
            )
            db.add(receipt)
            db.commit()

            self.assertEqual(total_model.receipts.count(), receipt.id)
            self.assertEqual(
                total_model.receipts.first().total_id, user.id)

        # db.delete(receipt)
        # db.delete(total_model)
        # db.delete(user)

        # self.assertIsNone(db.query(Total).filter(
        #     Total.id == total_model.id))
        # self.assertIsNone(db.query(User).filter(
        #     User.id == 1))

    def test_total_json(self):
        with self.TestSession() as db:
            user = User(username=os.getenv('MAIL_USERNAME'),
                        email=os.getenv('MAIL_USERNAME'),
                        password=os.getenv('PASSWORD'))

            db.add(user)
            db.commit()

            total_model = Total(totals, tax_totals, tax_year, user.id)

            db.add(total_model)
            db.commit()

            expected = {
                'id': total_model.id,
                'totals': json.dumps(totals, use_decimal=True),
                'tax_totals': json.dumps(tax_totals, use_decimal=True),
                'tax_year': tax_year,
                'user_id': user.id
            }

        self.assertDictEqual(total_model.serialize(), expected)
