
import pytest

from app.users import models
from app.tests.helpers import test_client, override_get_db, clear_test_db, create_test_token, Base, engine


def fill_db_with_necessary_data():
    user = models.User(email='test_email', password='test_password')
    db = override_get_db().__next__()
    # cleanup base before adding user
    db.query(models.User).delete()
    db.add(user)
    db.commit()

fill_db_with_necessary_data()

def test_get_users():    
    response = test_client.get(
        "/users/",
    )
    assert response.status_code == 200
    data = response.json()
    assert data[0]['email'] == 'test_email'
    assert data[0]['password'] == 'test_password'

def test_get_users_with_pagination():
    user = models.User(email='test_email_2', password='test_password_2')
    db = override_get_db().__next__()
    db.add(user)
    db.commit()
    response = test_client.get(
        "/users?skip=1&limit=1",
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['email'] == 'test_email_2'
    assert data[0]['password'] == 'test_password_2'

def test_get_user_me():
    response = test_client.get(
        "/users/me",
        headers={"Authorization": create_test_token()}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test_email"
    assert data["password"] == "test_password"
    assert data["id"] == 1

def test_get_user():    
    response = test_client.get(
        "/users/1",
        headers={"Authorization": create_test_token()}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test_email"

def test_get_user_with_invalid_token():
    response = test_client.get(
        "/users/1",
        headers={"Authorization": "token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail":"Not authenticated"}

def test_get_user_with_not_his_id():
    response = test_client.get(
        "/users/1",
        headers={"Authorization": create_test_token(email='test_email_2')}
    )
    assert response.status_code == 401
    data = response.json()
    assert data == {'detail': 'Could not validate credentials'}

def test_create_user():
    user = {"email": 'test_email_3', "password": "test_password_3"}
    response = test_client.post(
        "/users",
        json=user
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test_email_3"
    assert data["id"] == 3

def test_create_user_with_existing_email():
    user = {"email": 'test_email', "password": "test_password_3"}
    response = test_client.post(
        "/users",
        json=user
    )
    assert response.status_code == 400
    data = response.json()
    assert data == {'detail': 'User already exist'}