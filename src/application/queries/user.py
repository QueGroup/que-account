from typing import (
    Any,
)

from sqlalchemy import (
    Select,
    Update,
    select,
    update,
)

from src.application import (
    dto,
)
from src.application.mixins.base import (
    CRUDMixin,
)
from src.domain.user import (
    entity,
)
from src.infrastructure.database import (
    models,
)


class UserQuery(CRUDMixin[models.User, entity.User, dto.UserUpdate]):
    def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        return select(self.model).filter(*args).filter_by(**kwargs)

    def _get_all_query(
            self, skip: int = 0, limit: int = 10, *args: Any, **kwargs: Any
    ) -> Select[tuple[Any]]:
        return select(self.model).offset(skip).limit(limit).filter(*args).filter_by(**kwargs)

    def _update_query(self, pk: int, data_in: dto.UserUpdate, **kwargs: Any) -> Update:
        return (
            update(self.model)
            .where(self.model.id == pk)
            .values(**data_in.model_dump(exclude_unset=True))
            .filter_by(**kwargs)
            .returning(self.model)
        )

    def _delete_query(self, *args: Any, **kwargs: Any) -> Update:
        return (
            update(self.model)
            .where(self.model.id == kwargs.get("id"))
            .values(is_active=kwargs.get("is_active"))
        )
