from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
)
from starlette import (
    status,
)

from src.application import (
    dto,
)
from src.application.dto import (
    ProfileCreatePrivate,
)
from src.application.services.profile import (
    ProfileService,
)
from src.infrastructure.database import (
    models,
)
from src.presentation.api.providers import (
    Container,
    get_current_user,
)

profile_router = APIRouter()


@profile_router.post(
    "/",
    response_model=dto.Profile,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)]
)
@inject
async def create_profile(
        profile_in: dto.ProfileCreate,
        profile_service: ProfileService = Depends(Provide[Container.profile_service]),
        user: models.User = Depends(get_current_user)
) -> models.Profile:
    profile_in = ProfileCreatePrivate(**profile_in.model_dump(), user_id=user.id)
    return await profile_service.create_profile(profile_in=profile_in)
