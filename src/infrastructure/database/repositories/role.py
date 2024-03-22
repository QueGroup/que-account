from typing import (
    Callable,
)

from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from src.application.repositories import (
    RoleQueryMixin,
)
from src.infrastructure.database.models import (
    RoleModel,
)


class RoleRepository(RoleQueryMixin):
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        super().__init__(session=session_factory, model=RoleModel)
