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
from src.application.dto import (
    ResetPassword,
)
from src.application.service import (
    AuthService,
)
from src.application.strategies import (
    DefaultAuthStrategy,
    TelegramAuthStrategy,
)
from src.infrastructure.database import (
    models,
)
from src.infrastructure.services.security import (
    JWTService,
)
from src.presentation.api.providers import (
    Container,
    refresh_tokens,
    verify_token_from_request,
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
        response: Response,
        auth_service: AuthService = Depends(Provide[Container.auth_service]),
) -> dto.JWTokens:
    strategy = DefaultAuthStrategy()
    jwt_tokens = await auth_service.signin(user_in=user_in, strategy=strategy)
    JWTService.set_cookies(
        response=response,
        access_token=jwt_tokens.access_token,
        refresh_token=jwt_tokens.refresh_token,
    )

    return jwt_tokens


@auth_router.post(
    "/refresh/",
    response_model=dto.JWTokens,
    summary="Write out new pair of jwt tokens",
    status_code=status.HTTP_200_OK,
)
async def refresh_token(
        request: Request,
        response: Response
) -> dto.JWTokens:
    return await refresh_tokens(
        request=request,
        response=response,
    )


@auth_router.post(
    "/verify/",
    summary="Verification of the transmitted access_token",
    status_code=status.HTTP_200_OK,
)
async def verify_token(
        request: Request,
) -> bool:
    return await verify_token_from_request(
        request=request,
    )


# TODO: Эта точка должна быть доступна только авторизованному пользователю
@auth_router.post(
    "/reset_password/",
    status_code=status.HTTP_200_OK,
)
async def reset_password(
        password_in: ResetPassword
) -> None:
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
        otp_in: dto.ConfirmOtp,
        request: Request,
        response: Response,
) -> None:
    pass
