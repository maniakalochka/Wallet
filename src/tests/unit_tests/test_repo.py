import pytest

from models.user import User
from repositories.user import UserRepo


@pytest.mark.parametrize("id, exists", [(1, True), (2, True), (4, False)])
async def test_find_by_id(id, exists):
    repo = UserRepo()
    user = await repo.find_by_id(id)
    if exists:
        assert user
        assert user.id == id
    else:
        assert user is None


@pytest.mark.parametrize("id", [1, 2, 3])
async def test_can_deactivate_user(id):
    repo = UserRepo()
    user = await repo.deactivate_user(id)
    assert user["status_code"] == 200
    assert user["transaction"] == "Successful"
