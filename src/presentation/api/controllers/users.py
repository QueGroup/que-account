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
    HTTPException,
    Path,
    status,
)

from src.application.dto import (
    UserResponseSchema,
    UserUpdateSchema,
)
from src.application.service import (
    UserService,
)
from src.infrastructure.database.models import (
    UserModel,
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
    response_model=list[UserResponseSchema],
    status_code=status.HTTP_200_OK
)
@inject
async def get_list(
        user_service: UserService = Depends(Provide[Container.user_service]),
) -> list[UserModel]:
    return await user_service.get_users()


@user_router.get(
    "/me/{user_id}/",
    summary="Getting user details",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK
)
@inject
async def get_user(
        user_id: int,
        current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    if current_user.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    if not current_user.is_active:
        raise UserDeactivatedError()
    return current_user


@user_router.patch(
    "/me/{user_id}/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_200_OK,
)
@inject
async def update_user(
        user_id: Annotated[int, Path],
        user_in: UserUpdateSchema,
        current_user: UserModel = Depends(get_current_user),
        user_service: UserService = Depends(Provide[Container.user_service])
) -> UserModel:
    if current_user.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return await user_service.update_user(pk=user_id, user_in=user_in)


@user_router.delete(
    "/me/{user_id}/",
    summary="Deactivate user account",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def deactivate_user(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service])
) -> None:
    return await user_service.deactivate_user(user_id=user_id)
