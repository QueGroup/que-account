import dataclasses
from datetime import (
    datetime,
)

from src.infrastructure.services.security import (
    HashService,
)
from src.core import (
    ex,
)


@dataclasses.dataclass
class User:
    username: str
    password: str | None = None
    telegram_id: int | None = None
    confirmation_code: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    deleted_at: datetime | None = None
    language: str = "ru"

    @classmethod
    def create(
            cls,
            password: str | None,
            telegram_id: int | None,
            username: str,
    ) -> "User":
        if not password and not telegram_id:
            raise ex.MissingFieldsError(fields=["telegram_id", "password"])

        return cls(
            password=HashService.hash_password(password) if password else None,
            telegram_id=telegram_id if telegram_id else None,
            username=username,
        )

    @classmethod
    def set_password(cls, password: str) -> None:
        cls.password = HashService.hash_password(password=password)

    @classmethod
    def check_password(cls, password_in: str, password: str | None = None) -> bool:
        if not password and not password_in:
            raise ex.MissingFieldsError(fields=["password"])
        if password is None:
            password = cls.password
        return HashService.verify_password(password=password, hashed_password=password_in)
