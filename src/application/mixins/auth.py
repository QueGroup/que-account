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
from src.infrastructure.database.models import (
    UserModel,
)

from .base import (
    AuthMixin,
)


class AuthQueryMixin(AuthMixin[UserModel, UserEntity]):

    def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        username_f = UserModel.username == kwargs.get("username")
        telegram_id_f = UserModel.telegram_id == kwargs.get("telegram_id")

        combined_filter = or_(username_f, telegram_id_f)

        return select(UserModel).filter(combined_filter)
