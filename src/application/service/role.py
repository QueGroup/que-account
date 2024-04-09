from src.application import (
    dto,
)
from src.infrastructure.database import (
    models,
)
from src.infrastructure.database.repositories.role import (
    RoleRepository,
)


class RoleService:

    def __init__(self, role_repository: RoleRepository):
        self.repository = role_repository

    async def create_role(self, role_in: dto.RoleCreate) -> models.Role:
        return await self.repository.create(data_in=role_in)

    async def get_role_by_id(self, role_id: int) -> models.Role | None:
        return await self.repository.get_single(id=role_id)

    async def get_role_by_title(self, title: str) -> models.Role | None:
        return await self.repository.get_single(title=title)

    async def get_all_roles(self) -> list[models.Role]:
        return await self.repository.get_multi()

    async def update_role(self, pk: int, role_in: dto.RoleUpdate) -> models.Role:
        return await self.repository.partial_update(pk=pk, data_in=role_in)

    async def delete_role(self, role_id: int) -> None:
        return await self.repository.destroy(id=role_id)
