from httpx import (
    AsyncClient,
)
import pytest
from starlette import (
    status,
)


@pytest.mark.asyncio
async def test_profile_create_and_get(ac: AsyncClient) -> None:
    body = {
        "username": "username",
        "password": "<PASSWORd>1"
    }

    create_response = await ac.post("/api/v1/auth/signup/", json=body)
    assert create_response.status_code == status.HTTP_201_CREATED

    login_response = await ac.post("/api/v1/auth/login/",
                                   json={"username": "username", "password": "<PASSWORd>1"})
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # TODO: Заменить данные на fake generator
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
    get_user_response = await ac.get("/api/v1/users/me/", headers=headers)
    assert get_user_response.json()["profile"] is not None
    assert get_user_response.json()["profile"]["user_id"] == get_user_response.json()["id"]


@pytest.mark.asyncio
async def test_profile_update(ac):
    body = {
        "username": "username",
        "password": "<PASSWORd>1"
    }

    create_response = await ac.post("/api/v1/auth/signup/", json=body)
    assert create_response.status_code == status.HTTP_201_CREATED

    login_response = await ac.post("/api/v1/auth/login/",
                                   json={"username": "username", "password": "<PASSWORd>1"})
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # TODO: Заменить данные на fake generator
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

    profile_id = profile_create_response.json()["id"]
    updated_data = {
        "city": "Los Angeles"
    }
    update_response = await ac.patch(f"/api/v1/profiles/{profile_id}", headers=headers, json=updated_data)
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json()["city"] == updated_data["city"]


@pytest.mark.asyncio
async def test_profile_delete(ac):
    body = {
        "username": "username",
        "password": "<PASSWORd>1"
    }

    create_response = await ac.post("/api/v1/auth/signup/", json=body)
    assert create_response.status_code == status.HTTP_201_CREATED

    login_response = await ac.post("/api/v1/auth/login/",
                                   json={"username": "username", "password": "<PASSWORd>1"})
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # TODO: Заменить данные на fake generator
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

    profile_id = profile_create_response.json()["id"]
    response = await ac.delete(f"/api/v1/profiles/{profile_id}", headers=headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    get_user_response = await ac.get("/api/v1/users/me/", headers=headers)
    assert get_user_response.json()["profile"] is None
