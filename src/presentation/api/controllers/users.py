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
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jose import (
    jwt,
)

from src.application.dto import (
    TokenData,
    UserResponseSchema,
)
from src.application.service import (
    UserService,
)
from src.infrastructure import (
    Config,
)
from src.infrastructure.database.models import (
    UserModel,
)
from src.presentation.api.di_containers import (
    Container,
)
from src.presentation.api.exceptions import (
    UserDeactivatedError,
)

user_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@inject
async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        config: Config = Depends(Provide[Container.config]),
        user_service: UserService = Depends(Provide[Container.user_service]),
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.security.secret_key, algorithms=[config.security.algorithm])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except jwt.JWTError:
        raise credentials_exception
    user = await user_service.get_user(user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


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
    "/{user_id}/",
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


@user_router.delete(
    "/{user_id}/",
    summary="Deactivate user account",
    status_code=status.HTTP_204_NO_CONTENT
)
@inject
async def deactivate_user(
        user_id: int,
        user_service: UserService = Depends(Provide[Container.user_service])
) -> None:
    return await user_service.delete_user(user_id=user_id)
