from src.application import (
    dto,
)
from src.application.dto import (
    ProfileCreate,
)
from src.infrastructure.database import (
    models,
)
from src.infrastructure.database.repositories import (
    ProfileRepository,
)


class ProfileService:
    def __init__(self, profile_repository: ProfileRepository):
        self.repository: ProfileRepository = profile_repository

    async def get_profiles(self) -> list[models.Profile]:
        return await self.repository.get_multi()

    async def get_profile_by_id(self, user_id: int) -> models.Profile | None:
        return await self.repository.get_single(user_id=user_id)

    async def create_profile(self, profile_in: dto.ProfileCreate, user_id: int) -> models.Profile:
        profile_in = ProfileCreate(**profile_in.model_dump(), user_id=user_id)
        return await self.repository.create(data_in=profile_in)

    async def update_profile(self, profile_in: dto.ProfileUpdate, profile_id: int) -> models.Profile:
        return await self.repository.partial_update(data_in=profile_in, pk=profile_id)

    # FIXME: Не факт, что работает корректно
    async def delete_profile(self, profile_id: int) -> None:
        return await self.repository.destroy(id=profile_id)
