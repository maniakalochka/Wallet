import pytest


@pytest.mark.parametrize(
    "email, password, status_code, username",
    [
        ("jd@example.com", "password", 200, "johndoe"),
        ("jd@example.com", "password1", 400, "johndoe"),
        ("pes@kot.ru", "pessokot", 200, "pes"),
    ],
)
async def test_user_can_create_account(email, password, status_code, username, client):
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "username": username,
        "email": email,
        "hashed_password": password,
        "is_active": True,
        "is_admin": False,
    }

    response = client.post("/auth/", json=payload)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "username, password, status_code", [("johndoe45", "password", 200)]
)
async def test_user_can_login(username, password, status_code, client):
    # Создаем пользователя для теста
    create_payload = {
        "first_name": "John",
        "last_name": "Doe",
        "username": username,
        "email": "jh45@example.com",
        "hashed_password": password,
        "is_active": True,
        "is_admin": False,
    }
    create_response = client.post("/auth/", json=create_payload)
    assert create_response.status_code == status_code

    # Выполняем вход
    login_payload = {
        "username": username,
        "password": password,
    }
    response = client.post("/auth/login", data=login_payload)
    print(response.json())
    assert response.status_code == status_code
