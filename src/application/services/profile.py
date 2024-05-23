from src.application import (
    dto,
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

    async def get_profile_by_id(self, profile_id: int) -> models.Profile | None:
        return await self.repository.get_single(id=profile_id)

    async def create_profile(self, profile_in: dto.ProfileCreate) -> models.Profile:
        return await self.repository.create(data_in=profile_in)
