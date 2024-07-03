from typing import (
    Any,
)

from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    status,
)

from src.application.services import (
    PhotoService,
)
from src.infrastructure.database import (
    models,
)
from src.presentation.api import (
    dto,
)
from src.presentation.api.providers import (
    Container,
    get_current_user,
)

photo_router = APIRouter()


@photo_router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=dto.PhotoUploadResponse,
)
@inject
async def upload_photo(
        file: UploadFile = File(...),
        user: models.User = Depends(get_current_user),
        photo_service: PhotoService = Depends(Provide[Container.photo_service])
) -> Any:
    return await photo_service.upload_file(user_id=user.id, file=file)


@photo_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=dto.PhotosResponse,
)
@inject
async def get_all_user_photos(
        user: models.User = Depends(get_current_user),
        photo_service: PhotoService = Depends(Provide[Container.photo_service])
) -> Any:
    return await photo_service.get_all_photos(user_id=user.id)
