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
async def test_sign_up_default(ac: AsyncClient) -> None:
    body = {
        "username": fake.user_name(),
        "password": fake.password(length=9)
    }

    response = await ac.post(
        url="/api/v1/auth/signup/",
        json=body
    )
    assert "username" in response.json()
    assert response.status_code == 201


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
    ]
)
async def test_sign_up(ac: AsyncClient, body, expected_status, expected_detail) -> None:
    response = await ac.post(
        url="/api/v1/auth/signup/",
        json=body
    )

    assert response.json()["detail"] == expected_detail
    assert response.status_code == expected_status
