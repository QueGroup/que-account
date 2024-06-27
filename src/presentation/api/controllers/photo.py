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
)

from src.application.services import (
    PhotoService,
)
from src.infrastructure.database import (
    models,
)
from src.presentation.api.providers import (
    Container,
    get_current_user,
)

photo_router = APIRouter()


@photo_router.post("/")
@inject
async def upload_photo(
        file: UploadFile = File(...),
        user: models.User = Depends(get_current_user),
        photo_service: PhotoService = Depends(Provide[Container.photo_service])
) -> Any:
    return await photo_service.upload_file(user_id=user.id, file=file)


@photo_router.get("/")
@inject
async def get_all_user_photos(
        user: models.User = Depends(get_current_user),
        photo_service: PhotoService = Depends(Provide[Container.photo_service])
) -> Any:
    return await photo_service.get_all_photos(user_id=user.id)
