import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient
from models.user import User


base_url = "http://127.0.0.1:8000/auth"


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(base_url=base_url) as client:
        yield client


@pytest.mark.asyncio
@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
async def test_create_user_success(mock_post, async_client: AsyncClient):
    mock_data = [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "password": "password",
            "is_admin": False,
        }
    ]

    mock_post.return_value.status_code = 201
    mock_post.return_value.json = AsyncMock(return_value=mock_data)

    response = await async_client.post("/")
    assert response.status_code == 201
    json_response = await response.json()
    assert json_response == mock_data
