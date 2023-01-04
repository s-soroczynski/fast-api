import pytest

from app.tests.helpers import override_get_db, create_pure_test_token
from app.users.utils import authenticate_user, get_current_user


def test_authenticate_user():
    db = override_get_db().__next__()
    authenticated_user = authenticate_user(username="test_email",password="test_password",db=db)
    assert authenticated_user.email == "test_email"

@pytest.mark.asyncio
async def test_get_current_user():
    db = override_get_db().__next__()
    token = create_pure_test_token()
    user = await get_current_user(token=token, db=db)
    assert user.email == "test_email"
    assert user.id == 1
