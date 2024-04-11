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
from src.application.services import (
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
from src.presentation.api.exceptions import (
    PasswordIncorrectError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.presentation.api.providers import (
    Container,
    get_current_user,
    refresh_tokens,
    verify_token_from_request,
)
from src.shared import (
    ex,
)

auth_router = APIRouter()


@auth_router.post(
    "/signup/",
    response_model=dto.UserResponse,
    responses={409: {"message": "User already exists"}},
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
@inject
async def signup(
        user_in: dto.UserRegistration,
        auth_service: AuthService = Depends(Provide[Container.auth_service]),
) -> models.User:
    try:
        return await auth_service.signup(user_in=user_in)
    except ex.UserAlreadyExists:
        raise UserAlreadyExistsError()


@auth_router.post(
    "/login/t/me/",
    response_model=dto.JWTokens,
    responses={
        404: {"message": "Not found"},
        401: {"message": "Incorrect password"}
    },
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
    try:
        jwt_tokens = await auth_service.signin(user_in=user_in, strategy=strategy)
    except ex.UserNotFound:
        raise UserNotFoundError()
    except ex.IncorrectPassword:
        raise PasswordIncorrectError()
    return jwt_tokens


@auth_router.post(
    "/login/",
    response_model=dto.JWTokens,
    responses={
        404: {"message": "Not found"},
        401: {"message": "Incorrect password"}
    },
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
    try:
        jwt_tokens = await auth_service.signin(user_in=user_in, strategy=strategy)
        JWTService.set_cookies(
            response=response,
            access_token=jwt_tokens.access_token,
            refresh_token=jwt_tokens.refresh_token,
        )
    except ex.UserNotFound:
        raise UserNotFoundError()
    except ex.IncorrectPassword:
        raise PasswordIncorrectError()

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


# TODO: Необходимо инвалидировать текущий JWT-токен после сброса пароля:
#  Теперь нужно сохранять идентификатор токена (token ID) в базе данных при его создании.
#  При сбросе пароля удалите все токены, связанные с текущим пользователем, из базы данных.
#  Создайте новый JWT-токен и верните его клиенту.
@auth_router.post(
    "/reset_password/",
    status_code=status.HTTP_200_OK,
)
@inject
async def reset_password(
        password_in: ResetPassword,
        current_user: Annotated[models.User, Depends(get_current_user)],
        auth_service: AuthService = Depends(Provide[Container.auth_service]),
) -> Response:
    await auth_service.reset_password(pk=current_user.id, password_in=password_in)
    return Response(status_code=status.HTTP_200_OK, content="Password was updating")


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
