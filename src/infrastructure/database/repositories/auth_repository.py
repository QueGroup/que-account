from typing import (
    Callable,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from src.application.repositories import (
    AuthRepository,
)
from src.infrastructure.database.models import (
    UserModel,
)


class SQLAlchemyAuthRepository(AuthRepository):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        super().__init__(session=session_factory, model=UserModel)
