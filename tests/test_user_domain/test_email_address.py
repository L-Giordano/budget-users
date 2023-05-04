from unittest import TestCase
from parameterized import parameterized

from src.users.domain.email_address import EmailAddress


class TestEmailAddress(TestCase):

    def test_when_email_has_correct_format(self):
        email = 'juan@email.com'
        email_address = EmailAddress(email)
        self.assertTrue(type(email_address) == EmailAddress)
        self.assertEqual(email, email_address.value)

    @parameterized.expand(
            [
                ('juan'),
                ('juan.garcia.com'),
                ('juan@email'),
                ('juan_email.com'),
                ('juan@email_com'),
            ]
    )
    def test_when_email_has_incorrect_format(self, email):
        with self.assertRaises(ValueError):
            EmailAddress(email)
