from typing import (
    Callable,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from src.application.mixins import (
    AuthQueryMixin,
)
from src.infrastructure.database import (
    models,
)


class AuthRepository(AuthQueryMixin):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        super().__init__(session=session_factory, model=models.UserModel)
