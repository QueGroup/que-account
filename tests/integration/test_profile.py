from httpx import (
    AsyncClient,
)
import pytest
from starlette import (
    status,
)


@pytest.fixture(scope="session")
async def user_and_profile(ac: AsyncClient) -> None:
    body = {
        "username": "testtusername",
        "password": "<PASSWORd>1"
    }

    create_response = await ac.post("/api/v1/auth/signup/", json=body)
    assert create_response.status_code == status.HTTP_201_CREATED

    login_response = await ac.post("/api/v1/auth/login/",
                                   json={"username": "testtusername", "password": "<PASSWORd>1"})
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "first_name": "John",
        "gender": "male",
        "city": "New York",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "birthdate": "2005-05-23",
        "description": "I like sports and music",
        "interested_in": "women",
        "hobbies": [
            "sports", "music"
        ]
    }

    profile_create_response = await ac.post("/api/v1/profiles/", json=data, headers=headers)
    assert profile_create_response.status_code == status.HTTP_201_CREATED

    yield token, headers, profile_create_response


@pytest.mark.asyncio
async def test_create_and_get_profile(ac, user_and_profile):
    token, headers, _ = user_and_profile

    get_user_response = await ac.get("/api/v1/users/me/", headers=headers)
    assert get_user_response.json()["profile"] is not None
    assert get_user_response.json()["profile"]["user_id"] == get_user_response.json()["id"]


@pytest.mark.asyncio
async def test_get_profile(ac, user_and_profile):
    token, headers, _ = user_and_profile
    get_user_response = await ac.get("/api/v1/users/me/", headers=headers)
    profile_response = await ac.get(f"/api/v1/profiles/{get_user_response.json().get('id')}", headers=headers)
    assert profile_response.json() is not None


# TODO: Проверить, что именно выбрасывается 404 ошибка
@pytest.mark.asyncio
@pytest.mark.xfail
async def test_get_none_profile(ac, user_and_profile):
    token, headers, _ = user_and_profile
    profile_response = await ac.get(f"/api/v1/profiles/{999}", headers=headers)
    assert profile_response.json() is None


@pytest.mark.asyncio
async def test_profile_update(ac, user_and_profile):
    token, headers, profile_create_response = user_and_profile
    profile_id = profile_create_response.json()["id"]
    updated_data = {
        "city": "Los Angeles"
    }
    update_response = await ac.patch(f"/api/v1/profiles/{profile_id}", headers=headers, json=updated_data)
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["city"] == updated_data["city"]


@pytest.mark.asyncio
async def test_profile_delete(ac, user_and_profile):
    token, headers, profile_create_response = user_and_profile

    profile_id = profile_create_response.json()["id"]
    response = await ac.delete(f"/api/v1/profiles/{profile_id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    get_user_response = await ac.get("/api/v1/users/me/", headers=headers)
    assert get_user_response.json()["profile"] is None
