from dataclasses import (
    dataclass,
)

from src.domain.common import (
    DomainException,
)


@dataclass(eq=False)
class UserNotFound(DomainException):
    status = 404
    user_id: int

    @property
    def title(self) -> str:
        return f"UserEntity with ID {self.user_id} not found"


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
