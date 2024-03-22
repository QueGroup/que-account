from typing import (
    Any,
)

from sqlalchemy import (
    Delete,
    Select,
    Update,
    select,
    update,
)

from src.application.dto import (
    RoleCreateSchema,
    RoleUpdateSchema,
)
from src.infrastructure.database.models import (
    RoleModel,
)

from .abс_repository import (
    CRUDMixin,
    UpdateSchemaT,
)


class RoleQueryMixin(CRUDMixin[RoleModel, RoleCreateSchema, RoleUpdateSchema]):
    def _get_query(self, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        return select(self.model).filter(*args).filter_by(**kwargs)

    def _get_all_query(self, skip: int = 0, limit: int = 10, *args: Any, **kwargs: Any) -> Select[tuple[Any]]:
        return select(
            self.model
        ).offset(skip).limit(limit).filter(*args).filter_by(**kwargs).order_by(self.model.role_id)

    def _update_query(self, pk: int, data_in: UpdateSchemaT, **kwargs: Any) -> Update:
        return (
            update(
                self.model
            ).where(
                self.model.role_id == pk
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

    def _delete_query(self, *args: Any, **kwargs: Any) -> Delete:
        return Delete(self.model).filter(*args)
