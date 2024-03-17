from typing import (
    Any,
)

from sqlalchemy import (
    Delete,
    Select,
    Update,
    or_,
    select,
)

from src.domain.user.entites import (
    UserEntity,
)
from src.infrastructure.database.models import (
    UserModel,
)

from .abс_repository import (
    AbstractAuthRepository,
    AbstractRefreshTokenRepository,
    UpdateSchemaT,
)


class AuthRepository(AbstractAuthRepository[UserModel, UserEntity]):
    def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        username_f = UserModel.username == kwargs.get("username")
        telegram_id_f = UserModel.telegram_id == kwargs.get("telegram_id")

        combined_filter = or_(username_f, telegram_id_f)

        return select(UserModel).filter(combined_filter)

    def _get_all_query(self, skip: int = 0, limit: int = 10, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        pass

    def _update_query(self, data_in: UpdateSchemaT, **kwargs: Any) -> Update:
        pass

    def _delete_query(self, **kwargs: Any) -> Delete:
        pass


class RefreshTokenRepository(AbstractRefreshTokenRepository):

    def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        pass

    def _get_all_query(self, skip: int = 0, limit: int = 10, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        pass

    def _update_query(self, data_in: UpdateSchemaT, **kwargs: Any) -> Update:
        pass

    def _delete_query(self, **kwargs: Any) -> Delete:
        pass
