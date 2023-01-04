from app.tests.helpers import (
    test_client,
)
from app.security import pwd_context

hashed_password = pwd_context.hash("test_password")


def test_login():
    form_data = {"username": "test_email", "password": "test_password"}
    response = test_client.post("/login", data=form_data)
    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"


def test_login_with_no_existing_user():
    form_data = {"username": "test_email_100", "password": "test_password"}
    response = test_client.post("/login", data=form_data)
    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Incorrect username or password"}
