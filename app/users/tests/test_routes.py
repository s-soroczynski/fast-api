from app.users.models import User
from app.tests.helpers import test_client, create_test_token, add_model_to_db
from app.security import pwd_context

hash_test_password = pwd_context.hash("test_password")
test_user = User(email="test_email", password=hash_test_password)


def test_get_users():
    response = test_client.get(
        "/users/",
    )
    assert response.status_code == 200
    data = response.json()
    assert data[0]["email"] == "test_email"
    assert data[0]["password"] == hash_test_password


def test_get_users_with_query_params():
    user = User(email="test_email_2", password="test_password_2")
    add_model_to_db(user)
    response = test_client.get(
        "/users?skip=1&limit=1",
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == "test_email_2"
    assert data[0]["password"] == "test_password_2"


def test_get_user_me():
    response = test_client.get(
        "/users/me", headers={"Authorization": create_test_token()}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test_email"
    assert data["password"] == hash_test_password


def test_get_user():
    response = test_client.get(
        "/users/1", headers={"Authorization": create_test_token()}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test_email"


def test_get_user_with_invalid_token():
    response = test_client.get("/users/1", headers={"Authorization": "token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_user_with_not_his_id():
    response = test_client.get(
        "/users/1", headers={"Authorization": create_test_token(email="test_email_2")}
    )
    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Could not validate credentials"}


def test_create_user():
    user = {"email": "test_email_3", "password": "test_password_3"}
    response = test_client.post("/users", json=user)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test_email_3"


def test_create_user_with_existing_email():
    user = {"email": "test_email", "password": "test_password_3"}
    response = test_client.post("/users", json=user)
    assert response.status_code == 400
    data = response.json()
    assert data == {"detail": "User already exist"}
