import dataclasses
from datetime import (
    datetime,
)

from src.infrastructure.services.security import (
    HashService,
)


@dataclasses.dataclass
class UserEntity:
    username: str
    password: str | None = None
    telegram_id: int | None = None
    confirmation_code: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    deleted_at: datetime | None = None
    language: str = 'ru'

    @classmethod
    def create(
            cls,
            password: str,
            telegram_id: int | None,
            username: str,

    ) -> 'UserEntity':
        if password:
            hashed_password = HashService.hash_password(password)
            return cls(
                password=hashed_password,
                username=username
            )
        return cls(
            telegram_id=telegram_id,
            username=username
        )

    @classmethod
    def set_password(cls, password: str) -> None:
        cls.password = HashService.hash_password(password=password)

    @classmethod
    def check_password(cls, password: str) -> bool:
        return HashService.verify_password(password=password, hashed_password=cls.password)
