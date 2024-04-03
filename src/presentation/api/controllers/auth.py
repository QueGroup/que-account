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
    Request,
    Response,
    status,
)

from src.application import (
    dto,
)
from src.application.service import (
    AuthService,
)
from src.application.strategies import (
    DefaultAuthStrategy,
    TelegramAuthStrategy,
)
from src.infrastructure import (
    Config,
)
from src.infrastructure.database import (
    models,
)
from src.presentation.api.providers import (
    Container,
)

auth_router = APIRouter()


# FIXME: Теперь при создании пользователя задается роль по умолчанию, но я не тестировал как это работает.
#  так что возможны ошибки
@auth_router.post(
    "/signup/",
    response_model=dto.UserResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
@inject
async def signup(
        user_in: dto.UserRegistration,
        auth_service: AuthService = Depends(Provide[Container.auth_service]),
) -> models.User:
    return await auth_service.signup(user_in=user_in)


@auth_router.post(
    "/login/t/me/",
    response_model=dto.JWTokens,
    summary="Login in telegram",
    description="Login with telegram_id",
    status_code=status.HTTP_200_OK,
)
@inject
async def signin_telegram(
        user_in: dto.UserTMELogin,
        request: Request,
        response: Response,
        auth_service: AuthService = Depends(Provide[Container.auth_service]),
) -> dto.JWTokens:
    strategy = TelegramAuthStrategy()
    jwt_tokens = await auth_service.signin(user_in=user_in, strategy=strategy)
    return jwt_tokens


@auth_router.post(
    "/login/",
    response_model=dto.JWTokens,
    summary="Default login",
    description="Login with username and password",
    status_code=status.HTTP_200_OK,
)
@inject
async def login(
        user_in: dto.UserLogin,
        request: Request,
        response: Response,
        auth_service: AuthService = Depends(Provide[Container.auth_service]),
        config: Config = Depends(Provide[Container.config]),
) -> dto.JWTokens:
    strategy = DefaultAuthStrategy()
    jwt_tokens = await auth_service.signin(user_in=user_in, strategy=strategy)

    response.set_cookie(
        key="access_token",
        value=jwt_tokens.access_token,
        max_age=config.security.access_expire_time_in_seconds,
        secure=False,
        httponly=True,
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=jwt_tokens.refresh_token,
        max_age=config.security.refresh_expire_time_in_seconds,
        secure=False,
        httponly=True,
        samesite="lax",
    )

    return jwt_tokens


@auth_router.post(
    "/refresh/",
    response_model=dto.JWTokens,
    summary="Write out new pair of jwt tokens",
    status_code=status.HTTP_200_OK,
)
async def refresh_token(
        refresh_token_in: dto.TokenRefresh,
) -> None:
    pass


@auth_router.post(
    "/verify/",
    summary="Verification of the transmitted access_token",
    status_code=status.HTTP_200_OK,
)
async def verify_token(
        access_token_in: dto.TokenVerify,
) -> None:
    pass


@auth_router.post(
    "/reset_password/",
    status_code=status.HTTP_200_OK,
)
async def reset_password() -> None:
    pass


@auth_router.post(
    "/logout/",
    summary="Logout from  the current session",
    status_code=status.HTTP_200_OK
)
async def logout() -> None:
    pass


@auth_router.post(
    "/logout_all/",
    summary="Logout from the all session",
    status_code=status.HTTP_200_OK
)
async def logout_all() -> None:
    pass


@auth_router.post(
    "/send-otp-code/",
    summary="Send otp code",
    status_code=status.HTTP_200_OK,
)
async def send_otp_code(user_in: dto.UserLoginWithOTP) -> None:
    pass


@auth_router.post(
    "/confirm-otp-code/",
    response_model=dto.JWTokens,
    summary="Confirm otp code and write out the code",
    status_code=status.HTTP_200_OK,
)
async def confirm_otp_code(
        refresh_token_storage: Any,
        otp_in: dto.ConfirmOtp,
        request: Request,
        response: Response,
) -> None:
    pass
