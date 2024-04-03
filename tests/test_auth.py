import random
from typing import (
    Any,
)

from faker import (
    Faker,
)
from httpx import (
    AsyncClient,
)
import pytest
from starlette import (
    status,
)

fake = Faker()


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
                    "username": fake.user_name(),
                    "password": "short"
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Password should be at least 8 characters long"
        ),
        (
                {
                    "username": fake.user_name(),
                    "password": "lowercaseonly"
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Password should contain both uppercase and lowercase letters"
        ),
        (
                {
                    "username": fake.user_name(),
                    "password": "NoSpecial1"
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Password should contain at least one special character"
        ),
        (
                {
                    "username": fake.user_name(),
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
                    "username": fake.user_name(),
                    "telegram_id": random.randint(10000000, 9999999999)
                },
                status.HTTP_201_CREATED,
                None,
        ),
        (
                {
                    "username": "invalid_username#",
                    "telegram_id": 1234567890,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "Name should contains only letters"
        ),
    ]
)
async def test_signup_telegram(
        ac: AsyncClient,
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
