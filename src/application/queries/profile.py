from typing import (
    Any,
)

from sqlalchemy import (
    Delete,
    Select,
    Update,
    delete,
    select,
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
from src.shared.types import (
    UpdateSchemaT,
)


class ProfileQuery(CRUDMixin[models.Profile, dto.ProfileCreate, dto.ProfileUpdate]):
    def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        return select(self.model).where(self.model.id == kwargs.get("id"))

    def _get_all_query(self, skip: int = 0, limit: int = 10, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        return select(self.model).offset(skip).limit(limit).filter(*args).filter_by(**kwargs)

    def _update_query(self, pk: int, data_in: UpdateSchemaT, **kwargs: Any) -> Update:
        pass

    def _delete_query(self, *args: Any, **kwargs: Any) -> Delete:
        return delete(self.model).where(self.model.id == kwargs.get("id"))
