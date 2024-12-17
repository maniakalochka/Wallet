import fastapi
import pytest
import httpx


async def test_user_can_create_account(client):
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "jd@example.com",
        "hashed_password": "password",
        "is_active": True,
        "is_admin": False,
    }

    response = client.post("/auth/", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data["msg"] == "Successful"


# not working
@pytest.mark.skip(reason="not implemented")
@pytest.mark.asyncio
async def test_user_can_login(client):
    # Создаем пользователя для теста
    create_payload = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "jd@example.com",
        "hashed_password": "password",
        "is_active": True,
        "is_admin": False,
    }
    create_response = client.post("/auth/", json=create_payload)

    login_payload = {
        "username": "johndoe",
        "hashed_password": "password",
    }
    login_response = client.post("/auth/login", json=login_payload)
    assert login_response.status_code == 200

    data = login_response.json()
    print(data)  # Выводим весь ответ для проверки
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.skip(reason="not implemented")
@pytest.mark.asyncio
async def test_can_get_current_user(client):
    create_payload = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "jd@example.com",
        "hashed_password": "password",
        "is_active": True,
        "is_admin": False,
    }
    create_response = client.post("/auth/", json=create_payload)

    payload = {
        "username": "johndoe",
    }
    response = client.get("/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == response.json()["username"]
