from typing import (
    Callable,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from src.application.queries import (
    AuthQuery,
)
from src.infrastructure.database import (
    models,
)


class AuthRepository(AuthQuery):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        super().__init__(session=session_factory, model=models.User)
