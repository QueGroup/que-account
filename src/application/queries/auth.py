from typing import (
    Any,
)

from sqlalchemy import (
    Select,
    or_,
    select,
)

from src.application import (
    dto,
)
from src.application.persistence.base import (
    AuthMixin,
)
from src.domain.user import (
    entity,
)
from src.infrastructure.database import (
    models,
)


class AuthQuery(AuthMixin[models.User, entity.User, dto.ResetPassword]):

    def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        username_f = models.User.username == kwargs.get("username")
        if kwargs.get("telegram_id"):
            telegram_id_f = models.User.telegram_id == kwargs.get("telegram_id")
            combined_filter = or_(username_f, telegram_id_f)
        else:
            combined_filter = username_f
        return select(models.User).filter(combined_filter)

    def _get_user(self, *args: Any, **kwargs: Any) -> Select[tuple]:
        return select(self.model).filter(*args).filter_by(**kwargs)
