from src.application.dto import (
    RoleCreateSchema, RoleUpdateSchema,
)
from src.infrastructure.database.models import (
    RoleModel,
)
from src.infrastructure.database.repositories.role import (
    RoleRepository,
)


class RoleService:

    def __init__(self, role_repository: RoleRepository):
        self.repository = role_repository

    async def create_role(self, role_in: RoleCreateSchema) -> RoleModel:
        return await self.repository.create(data_in=role_in)

    async def get_role_by_id(self, role_id: int) -> RoleModel | None:
        return await self.repository.get_single(role_id=role_id)

    async def get_role_by_title(self, title: str) -> RoleModel | None:
        return await self.repository.get_single(title=title)

    async def get_all_roles(self) -> list[RoleModel]:
        return await self.repository.get_multi()

    async def update_role(self, pk: int, role_in: RoleUpdateSchema) -> RoleModel:
        return await self.repository.partial_update(pk=pk, data_in=role_in)

    async def delete_role(self, role_id: int) -> None:
        return await self.repository.destroy(role_id=role_id)
