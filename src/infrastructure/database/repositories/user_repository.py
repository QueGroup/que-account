from typing import (
    Callable,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from src.application.repositories.user_repository import (
    UserRepository,
)
from src.infrastructure.database.models import (
    UserModel,
)


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        super().__init__(session=session_factory, model=UserModel)
