from typing import (
    Any,
)

from sqlalchemy import (
    Select,
    Update,
    select,
    update,
)

from src.application.dto import (
    UserUpdateSchema,
)
from src.domain.user import (
    UserEntity,
)
from src.infrastructure.database.models import (
    UserModel,
)

from .base import (
    CRUDMixin,
    UpdateSchemaT,
)


class UserQueryMixin(CRUDMixin[UserModel, UserEntity, UserUpdateSchema]):
    def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        return select(self.model).filter(*args).filter_by(**kwargs)

    def _get_all_query(self, skip: int = 0, limit: int = 10, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        return select(self.model).offset(skip).limit(limit).filter(*args).filter_by(**kwargs)

    def _update_query(self, pk: int, data_in: UpdateSchemaT, **kwargs: Any) -> Update:
        return (
            update(
                self.model
            ).where(
                self.model.user_id == pk
            ).values(
                **data_in.model_dump(
                    exclude_unset=True
                )
            ).filter_by(
                **kwargs
            )
            .returning(
                self.model
            )
        )

    def _delete_query(self, *args: Any, **kwargs: Any) -> Update:
        return update(self.model).where(self.model.user_id == kwargs.get("user_id")).values(
            is_active=kwargs.get("is_active"))