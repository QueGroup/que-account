import time
from typing import (
    Any,
)

from httpx import (
    AsyncClient,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from starlette import (
    status,
)

from src.application import (
    services,
)
from src.core import (
    ex,
)
from src.infrastructure.database import (
    TelegramAuthStrategy,
)
from src.presentation.api import (
    dto,
)
from tests.misc import (
    fake,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body, expected_status, expected_detail",
    [
        (
                {
                    "username": "invalid_username#",
                    "password": fake.password(length=9)
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Name should contains only letters"
        ),
        (
                {
                    "username": fake.username(),
                    "password": fake.password(length=4)
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Password should be at least 8 characters long"
        ),
        (
                {
                    "username": fake.username(),
                    "password": "lowercaseonly"
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Password should contain both uppercase and lowercase letters"
        ),
        (
                {
                    "username": fake.username(),
                    "password": "NoSpecial1"
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Password should contain at least one special character"
        ),
        (
                {
                    "username": fake.username(),
                    "password": fake.password(length=9)
                },
                status.HTTP_201_CREATED,
                None
        )
    ]
)
async def test_signup_default(
        ac: AsyncClient,
        body: dict[str, Any],
        expected_status: int,
        expected_detail: str,
) -> None:
    response = await ac.post(
        url="/api/v1/auth/signup/",
        json=body
    )

    if expected_detail is not None:
        assert response.json()["detail"] == expected_detail
    assert response.status_code == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body, expected_status, expected_detail",
    [
        (
                {
                    "username": fake.username(),
                    "telegram_id": fake.telegram_id()
                },
                status.HTTP_201_CREATED,
                None,
        ),
        (
                {
                    "username": "invalid_username#",
                    "telegram_id": fake.telegram_id(),
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Name should contains only letters"
        ),
    ]
)
async def test_signup_telegram(
        ac: Any,
        body: dict[str, Any],
        expected_status: int,
        expected_detail: str | dict[str, Any],
):
    response = await ac.post(
        url="/api/v1/auth/signup/",
        json=body
    )
    if expected_detail is not None:
        assert response.json()["detail"] == expected_detail
    assert response.status_code == expected_status


async def create_test_user(ac, body: dict[str, Any]):
    response = await ac.post("/api/v1/auth/signup/", json=body)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_default_login(ac):
    username = fake.username()
    password = fake.password()

    body = {
        "username": username,
        "password": password
    }

    await create_test_user(ac=ac, body=body)

    expected_status = status.HTTP_200_OK

    login_response = await ac.post(
        url="/api/v1/auth/login/",
        json=body
    )
    assert login_response.status_code == expected_status
    assert "access_token" in login_response.json()
    assert "refresh_token" in login_response.json()


@pytest.mark.asyncio
async def test_login_wrong_password(ac):
    username = "username"
    password = "<PASSWORd>1"

    body = {
        "username": username,
        "password": password
    }

    await create_test_user(ac=ac, body=body)

    body["password"] = "<PASSWoRD>12"
    login_response = await ac.post(
        url="/api/v1/auth/login/",
        json=body
    )
    expected_status = status.HTTP_401_UNAUTHORIZED
    assert login_response.status_code == expected_status
    assert login_response.json()["detail"]["message"] == "Invalid username or password"


@pytest.mark.asyncio
async def test_login_not_found_user(ac) -> None:
    username = fake.username()
    password = "<PASSWORD>"
    body = {
        "username": username,
        "password": password
    }

    response = await ac.post(
        url="/api/v1/auth/login/",
        json=body
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail").get("message") == "User is not exists"


@pytest.mark.asyncio
async def test_login_telegram(ac: Any, mocker: MockerFixture) -> None:
    user_in = dto.UserTMELogin(
        telegram_id=12345,
        signature="test_signature",
        nonce=1,
        timestamp=int(time.time())
    )

    mock_signin = mocker.patch.object(services.AuthService, "signin")
    mock_signin.return_value = dto.JWTokens(access_token="test_access_token", refresh_token="test_refresh_token")

    response = await ac.post(
        url="/api/v1/auth/login/t/me/",
        json=user_in.model_dump()
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] == "test_access_token"
    assert response.json()["refresh_token"] == "test_refresh_token"

    assert mock_signin.call_args[1]['strategy'].__class__ == TelegramAuthStrategy


@pytest.mark.asyncio
async def test_signin_telegram_user_not_found(ac: Any, mocker: MockerFixture) -> None:
    user_in = dto.UserTMELogin(
        telegram_id=12345,
        signature="test_signature",
        nonce=1,
        timestamp=int(time.time())
    )

    mock_signin = mocker.patch.object(services.AuthService, "signin")
    mock_signin.side_effect = ex.UserNotFound()

    response = await ac.post(
        url="/api/v1/auth/login/t/me/",
        json=user_in.model_dump()
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail").get("message") == "User is not exists"
    assert mock_signin.call_args[1]['strategy'].__class__ == TelegramAuthStrategy


@pytest.mark.asyncio
async def test_signin_telegram_user_already_exists(ac: Any, mocker: MockerFixture) -> None:
    user_in = dto.UserTMELogin(
        telegram_id=12345,
        signature="test_signature",
        nonce=1,
        timestamp=int(time.time())
    )

    mock_signin = mocker.patch.object(services.AuthService, "signin")
    mock_signin.side_effect = ex.InvalidSignature()

    response = await ac.post(
        url="/api/v1/auth/login/t/me/",
        json=user_in.model_dump()
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail").get("message") == "Invalid signature"
    assert mock_signin.call_args[1]['strategy'].__class__ == TelegramAuthStrategy


@pytest.mark.asyncio
async def test_reset_password(ac: Any) -> None:
    pass


@pytest.mark.asyncio
async def test_logout(ac: Any) -> None:
    body = {
        "username": "testUsername",
        "password": "<PASSWORd>1"
    }
    await create_test_user(ac, body)

    lg_response = await ac.post(
        url="/api/v1/auth/login/",
        json=body
    )
    assert lg_response.status_code == status.HTTP_200_OK

    logout_response = await ac.post("/api/v1/auth/logout/")
    assert logout_response.status_code == status.HTTP_204_NO_CONTENT
    assert logout_response.content == b""

    user_response = await ac.get("/api/v1/users/me/")
    assert user_response.status_code == status.HTTP_401_UNAUTHORIZED
