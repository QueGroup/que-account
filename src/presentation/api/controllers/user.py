from typing import (
    Annotated,
)

from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
    status,
)

from src.application import (
    dto,
)
from src.application.service import (
    UserService,
)
from src.infrastructure.database import (
    models,
)
from src.presentation.api.exceptions import (
    UserDeactivatedError,
)
from src.presentation.api.providers import (
    Container,
    get_current_user,
)

user_router = APIRouter()


@user_router.get(
    "/",
    summary="Getting all users",
    response_model=list[dto.UserResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_list(
        user_service: UserService = Depends(Provide[Container.user_service]),
) -> list[models.UserModel]:
    return await user_service.get_users()


@user_router.get(
    "/me/",
    summary="Getting user details",
    response_model=dto.UserResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_user(
        current_user: Annotated[models.UserModel, Depends(get_current_user)],
) -> models.UserModel:
    if not current_user.is_active:
        raise UserDeactivatedError()
    return current_user


@user_router.patch(
    "/me/",
    response_model=dto.UserResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def update_user(
        user_in: dto.UserUpdate,
        current_user: Annotated[models.UserModel, Depends(get_current_user)],
        user_service: UserService = Depends(Provide[Container.user_service]),
) -> models.UserModel:
    return await user_service.update_user(pk=current_user.user_id, user_in=user_in)


@user_router.delete(
    "/me/{user_id}/",
    summary="Deactivate user account",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def deactivate_user(
        current_user: Annotated[models.UserModel, Depends(get_current_user)],
        user_service: UserService = Depends(Provide[Container.user_service]),
) -> None:
    return await user_service.deactivate_user(user_id=current_user.user_id)
