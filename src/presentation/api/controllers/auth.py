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

from src.application.dto import (
    ConfirmOtpSchema,
    JWTokensSchema,
    UserLoginSchema,
    UserLoginWithOTP,
    UserRegistrationSchema,
    UserResponseSchema,
    UserTMELoginSchema,
)
from src.application.service import (
    AuthService,
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

auth_router = APIRouter()


@auth_router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
@inject
async def signup(
        user_in: UserRegistrationSchema,
        auth_service: AuthService = Depends(Provide[Container.auth_service])
) -> UserModel:
    return await auth_service.signup(user_in=user_in)


@auth_router.post(
    "/login/t/me",
    response_model=JWTokensSchema,
    summary="Login in telegram",
    description="Login with telegram_id",
    status_code=status.HTTP_200_OK
)
async def signin_telegram(
        refresh_token_storage: Any,
        user_in: UserTMELoginSchema,
        request: Request,
        response: Response,
        user_service: Any,
):
    pass


@auth_router.post(
    "/login",
    response_model=JWTokensSchema,
    summary="Default login",
    description="Login with username and password",
    status_code=status.HTTP_200_OK
)
@inject
async def login(
        user_in: UserLoginSchema,
        request: Request,
        response: Response,
        auth_service: AuthService = Depends(Provide[Container.auth_service]),
        config: Config = Depends(Provide[Container.config])
) -> JWTokensSchema:
    jwt_tokens = await auth_service.signin(user_in=user_in)

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
    "/send-otp-code",
    summary="Send otp code",
    status_code=status.HTTP_200_OK,

)
async def send_otp_code(user_in: UserLoginWithOTP):
    pass


@auth_router.post(
    "/confirm-otp-code",
    response_model=JWTokensSchema,
    summary="Confirm otp code and write out the code",
    status_code=status.HTTP_200_OK,
)
async def confirm_otp_code(
        refresh_token_storage: Any,
        otp_in: ConfirmOtpSchema,
        request: Request,
        response: Response,
):
    pass


@auth_router.post(
    "/refresh",
    response_model=JWTokensSchema,
    summary="Write out new pair of jwt tokens",
    status_code=status.HTTP_200_OK
)
async def refresh_token():
    pass


@auth_router.post(
    "/verify",
    summary="Verification of the transmitted access_token",
    status_code=status.HTTP_200_OK
)
async def verify_token():
    pass


@auth_router.post(
    "/logout",
    summary="Logout from  the current session",
    status_code=status.HTTP_200_OK
)
async def logout():
    pass


@auth_router.post(
    "/logout_all",
    summary="Logout from the all session",
    status_code=status.HTTP_200_OK
)
async def logout_all():
    pass
