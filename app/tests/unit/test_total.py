import simplejson as json
from models import Total
from .unit_base_test import UnitBaseTest, error_message

total_model = Total(10.50, 5.00, '2022', 1)


class TotalTest(UnitBaseTest):
    def test_create_total(self):
        self.assertEqual(10.50, total_model.totals,
                         error_message('totals'))
        self.assertEqual(5.00, total_model.tax_totals,
                         error_message('tax_totals'))
        self.assertEqual('2022', total_model.tax_year,
                         error_message('tax_year'))
        self.assertEqual(1, total_model.user_id, error_message('user_id'))

    def test_total_serializer(self):
        expected = {
            'id': None,
            'totals': json.dumps(10.50, use_decimal=True),
            'tax_totals': json.dumps(5.00, use_decimal=True),
            'tax_year': '2022',
            'user_id': 1
        }

        self.assertDictEqual(expected, total_model.serialize())
