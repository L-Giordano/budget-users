from unittest import (
    TestCase,
    mock,
    )
from parameterized import parameterized

from src.users.domain.email_address import EmailAddress
from src.users.domain.errors import (
    PasswordError,
    UserError,
    )
from src.users.domain.password_encrypter import PasswordEncrypter
from src.users.domain.status import Status
from src.users.domain.user import User


class TestUser(TestCase):

    @mock.patch("src.users.domain.password_encrypter.PasswordEncrypter.new_ecrypted_password")
    def setup_user(mocked_hashed_password, other) -> User:

        mocked_hashed_password.return_value = 'password'

        first_name = 'Juan'
        last_name = 'Garcia'
        email = 'juangarcia@email.com'
        user_name = 'jgarcia'
        password = 'password'
        organization = []

        return User.create(first_name, last_name, email, user_name, password, organization)

    @mock.patch("src.users.domain.password_encrypter.PasswordEncrypter.new_ecrypted_password")
    def test_when_create_user_success(self, mocked_hashed_password):

        mocked_hashed_password.return_value = 'password'

        first_name = 'Juan'
        last_name = 'Garcia'
        email = 'juangarcia@email.com'
        user_name = 'jgarcia'
        password = 'password'
        organization = []

        user = User.create(first_name, last_name, email, user_name, password, organization)

        mocked_hashed_password.assert_called_once()

        self.assertEqual(first_name, user._first_name)
        self.assertEqual(last_name, user._last_name)
        self.assertEqual(email, user._email.value)
        self.assertEqual(user_name, user._user_name)
        self.assertTrue(user.is_active)

    @mock.patch("src.users.domain.password_encrypter.PasswordEncrypter.new_ecrypted_password")
    def test_when_create_user_success_without_passing_id(self, mocked_hashed_password):

        mocked_hashed_password.return_value = 'password'

        first_name = 'Juan'
        last_name = 'Garcia'
        email = 'juangarcia@email.com'
        user_name = 'jgarcia'
        password = 'password'
        organization = []
        user = User.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            user_name=user_name,
            password=password,
            organization=organization,
            )
        mocked_hashed_password.assert_called_once()

        self.assertEqual(first_name, user._first_name)
        self.assertEqual(last_name, user._last_name)
        self.assertEqual(email, user._email.value)
        self.assertEqual(user_name, user._user_name)
        self.assertTrue(user.is_active)

    @parameterized.expand(
            [
                ('change_personal_data', ()),
                ('change_email', ()),
                ('archive', ()),
                ('change_password', ()),
            ]
    )
    def test_when_try_to_modify_archived_user_throws_UserError(self, change_method, change_args):
        user = self.setup_user()
        user._status = Status.archived

        with self.assertRaises(UserError):
            user.modify_user(change_method=change_method, change_args=change_args)

    def test_when_try_to_change_personal_data_success(self):
        change_method = 'change_personal_data'
        new_first_name = 'Jose'
        new_last_name = 'Campanella'
        change_args = (new_first_name, new_last_name)

        user = self.setup_user()
        user.modify_user(change_method=change_method, change_args=change_args)

        self.assertEqual(new_first_name, user._first_name)
        self.assertEqual(new_last_name, user._last_name)

    def test_when_try_to_change_email_success(self,):
        change_method = 'change_email'
        new_email = 'jose@email.com'
        change_args = (new_email,)
        user = self.setup_user()
        user.modify_user(change_method=change_method, change_args=change_args)

        self.assertEqual(new_email, user._email.value)
        self.assertEqual(EmailAddress, type(user._email))

    def test_when_archive_user_success(self):
        change_method = 'archive'
        user = self.setup_user()
        user.modify_user(change_method=change_method)

        self.assertEqual(Status.archived, user._status)

    def test_when_change_password_throws_PasswordError(self):
        user = User.create(
            first_name='Bruno',
            last_name='Diaz',
            email='batman@email.com',
            user_name='batman',
            password='password',
            organization=[],
            )
        change_method = 'change_password'
        current_password = '_password'
        new_password = 'new_password'
        change_args = (current_password, new_password)
        with self.assertRaises(PasswordError):
            user.modify_user(change_method=change_method, change_args=change_args)

    def test_when_change_password_success(self):
        user = User.create(
            first_name='Bruno',
            last_name='Diaz',
            email='batman@email.com',
            user_name='batman',
            password='password',
            organization=[],
            )

        change_method = 'change_password'
        current_password = 'password'
        new_password = 'new_password'
        change_args = (current_password, new_password)

        user.modify_user(change_method=change_method, change_args=change_args)

        self.assertTrue(PasswordEncrypter.is_password_valid(new_password, user._password))
