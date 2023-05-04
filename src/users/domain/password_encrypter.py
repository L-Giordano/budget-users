import bcrypt


class PasswordEncrypter:

    @classmethod
    def new_ecrypted_password(cls, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    @classmethod
    def is_password_valid(cls, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
