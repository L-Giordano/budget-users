
from src.users.domain.email_address import EmailAddress
from src.users.domain.errors import (
    UserError,
    PasswordError,
    )
from src.users.domain.password_encrypter import PasswordEncrypter
from src.users.domain.status import Status
from src.organization.domain.organization import Organization


class User:
    def __init__(
            self,
            first_name: str,
            last_name: str,
            email: EmailAddress,
            user_name: str,
            password: str,
            organization: list[Organization],
            status: Status,
            id: str,
    ) -> None:
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._user_name = user_name
        self._password = password
        self._organization: organization
        self._status = status
        self._id = id

    @classmethod
    def create(
        cls,
        first_name: str,
        last_name: str,
        email: str,
        user_name: str,
        password: str,
        organization: list[Organization],
    ) -> "User":
        return cls(
            first_name,
            last_name,
            EmailAddress(email),
            user_name,
            PasswordEncrypter.new_ecrypted_password(password),
            organization,
            Status.active,
            id=None,
            )

    @property
    def is_active(self) -> bool:
        return self._status == Status.active

    def modify_user(self, change_method: str, change_args: tuple[str] = None) -> None:
        if self._status == Status.archived:
            raise UserError("Can not modify archived user!")

        change = getattr(self, change_method)
        change(*change_args) if change_args is not None else change()

    def change_personal_data(
            self,
            new_first_name: str,
            new_last_name: str,
            ) -> None:
        self._first_name = new_first_name
        self._last_name = new_last_name

    def change_email(self, new_email: str) -> None:
        self._email = EmailAddress(new_email)

    def archive(self) -> None:
        self._status = Status.archived

    def change_password(self, current_password, new_password) -> None:
        if not (PasswordEncrypter
                .is_password_valid(current_password, self._password)):
            raise PasswordError('You provided a wrong current password')
        self._password = PasswordEncrypter.new_ecrypted_password(new_password)
