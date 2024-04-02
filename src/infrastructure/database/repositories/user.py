from typing import (
    Callable,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from src.application.mixins.user import (
    UserQueryMixin,
)
from src.infrastructure.database import (
    models,
)


class UserRepository(UserQueryMixin):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        super().__init__(session=session_factory, model=models.UserModel)
