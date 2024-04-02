from typing import (
    Any,
)

from sqlalchemy import (
    Select,
    or_,
    select,
)

from src.domain.user.entity import (
    UserEntity,
)
from src.infrastructure.database import (
    models,
)

from .base import (
    AuthMixin,
)


class AuthQueryMixin(AuthMixin[models.UserModel, UserEntity]):

    def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        username_f = models.UserModel.username == kwargs.get("username")
        telegram_id_f = models.UserModel.telegram_id == kwargs.get("telegram_id")

        combined_filter = or_(username_f, telegram_id_f)

        return select(models.UserModel).filter(combined_filter)
