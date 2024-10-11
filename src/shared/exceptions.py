from dataclasses import (
    dataclass,
)

from src.domain.common import (
    DomainException,
)


class AuthExceptionCodes:
    """Auth errors codes mapping class"""

    USER_ALREADY_EXISTS: int = 3000
    NOT_FOUND: int = 3001
    USER_DEACTIVATED: int = 3002
    USER_UNAUTHORIZED: int = 3003
    PROVIDED_PASSWORD_INCORRECT: int = 3004
    INVALID_PROVIDED_TOKEN: int = 3005
    INVALID_SIGNATURE: int = 3006
    TOKEN_NOT_FOUND: int = 3007
    CREDENTIALS_INVALID: int = 3008
    OLD_PASSWORD_INVALID: int = 3009


@dataclass(eq=False)
class UserNotFound(DomainException):
    status = 404

    @property
    def title(self) -> str:
        return "User not found"


@dataclass(eq=False)
class ProfileNotFound(DomainException):
    status = 404

    @property
    def title(self) -> str:
        return "Profile not found"


@dataclass(eq=False)
class UserAlreadyExists(DomainException):
    status = 409
    username: str | None = None

    @property
    def title(self) -> str:
        return f"UserEntity with username {self.username} already exists"


@dataclass(eq=False)
class UsernameAlreadyExists(DomainException):
    username: str | None = None

    @property
    def title(self) -> str:
        if self.username is not None:
            return f'A user with the "{self.username}" username already exists'
        else:
            return "A user with the username already exists"


@dataclass(eq=False)
class UserNotActivated(DomainException):
    status = 403
    user_id: int

    @property
    def title(self) -> str:
        return f"UserEntity with ID {self.user_id} is not activated"


@dataclass(eq=False)
class UserIsNotSuperuser(DomainException):
    status = 403
    user_id: int

    @property
    def title(self) -> str:
        return f"UserEntity with ID {self.user_id} is not superuser"


@dataclass(eq=False)
class UserIsDeleted(DomainException):
    status = 403
    user_id: int

    @property
    def title(self) -> str:
        return f"UserEntity with ID {self.user_id} is deleted"


@dataclass(eq=False)
class MissingFieldsError(DomainException):
    status = 400
    fields: list[str]

    @property
    def title(self) -> str:
        field_names = ', '.join(self.fields)
        return f"You must specify one of the fields: {field_names}"


@dataclass(eq=False)
class IncorrectPassword(DomainException):
    status = 400

    @property
    def title(self) -> str:
        return "Input password is incorrect"


@dataclass(eq=False)
class InvalidSignature(DomainException):
    status = 422

    @property
    def title(self) -> str:
        return "Given signature is invalid"


@dataclass(eq=False)
class JWTDecodeError(Exception):
    status = 401

    @property
    def title(self) -> str:
        return "Decoding JSON Web Token failed"
