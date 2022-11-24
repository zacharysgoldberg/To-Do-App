from main import app
from unittest import TestCase

# [error message for unit tests]


class UnitBaseTest(TestCase):
    pass


def error_message(value):
    return f"The '{value}' of the receipt after creation does not equal the constructor argument."
