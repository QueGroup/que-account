from typing import (
    Any,
)

from sqlalchemy import (
    Delete,
    Select,
    Update,
    delete,
    select,
    update,
)

from src.application import (
    dto,
)
from src.application.persistence import (
    CRUDMixin,
)
from src.infrastructure.database import (
    models,
)
from src.shared import (
    UpdateSchemaT,
)


class ProfileQuery(CRUDMixin[models.Profile, dto.ProfileCreate, dto.ProfileUpdate]):
    def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        return select(self.model).where(self.model.user_id == kwargs.get("user_id"))

    def _get_all_query(self, skip: int = 0, limit: int = 10, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        return select(self.model).offset(skip).limit(limit).filter(*args).filter_by(**kwargs)

    def _update_query(self, pk: int, data_in: UpdateSchemaT, **kwargs: Any) -> Update:
        return (
            update(self.model)
            .where(self.model.id == pk)
            .values(**data_in.model_dump(exclude_unset=True))
            .filter_by(**kwargs)
            .returning(self.model)
        )

    def _delete_query(self, *args: Any, **kwargs: Any) -> Delete:
        return delete(self.model).where(self.model.id == kwargs.get("id"))
