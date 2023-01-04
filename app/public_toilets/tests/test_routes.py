
from app.tests.helpers import test_client, override_get_db, create_test_token, add_model_to_db
from app.public_toilets.models import PublicToilet
from app.users.models import User


def test_get_public_toilets():    
    response = test_client.get(
        "/public-toilets",
    )
    assert response.status_code == 200
    data = response.json()[0]
    assert data["description"] == "test_description"
    assert data["lat"] == 10.0
    assert data["lng"] == 10.0
    assert data["name"] == "test_name"
    assert data["rate"] == 1

def test_get_public_toilets_with_query_params():
    test_user_2 = User(email='test_email_2', password='test_password_2')
    test_public_toilet_2 = PublicToilet(name="test_name_2", description="test_description_2", lng=15, lat=15, rate=1, user=test_user_2)
    add_model_to_db(test_public_toilet_2)
    response = test_client.get(
        "/public-toilets?skip=1&limit=1",
    )
    assert response.status_code == 200
    data = response.json()[0]
    assert data["description"] == "test_description_2"
    assert data["lat"] == 15.0
    assert data["lng"] == 15.0
    assert data["name"] == "test_name_2"
    assert data["rate"] == 1

def test_get_public_toilet():    
    response = test_client.get(
        "/public-toilets/1",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "test_description"
    assert data["lat"] == 10.0
    assert data["lng"] == 10.0
    assert data["name"] == "test_name"
    assert data["rate"] == 1

def test_get_public_toilet_with_non_existing_id():    
    response = test_client.get(
        "/public-toilets/100",
    )
    assert response.status_code == 404
    data = response.json()
    assert data == {'detail': 'Public toilet with id 100 does not exist'}

def test_create_public_toilet():
    test_public_toilet_3 = {"name": "test_name_3", "description": "test_description_3", "lng": "10", "lat": "10", "rate":"1"}
    response = test_client.post(
        "/public-toilets",
        headers={"Authorization": create_test_token()},
        json=test_public_toilet_3
    )
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "test_description_3"
    assert data["lat"] == 10.0
    assert data["lng"] == 10.0
    assert data["name"] == "test_name_3"
    assert data["rate"] == 1

def test_create_public_toilet_with_existing_name():
    test_public_toilet_3 = {"name": "test_name_3", "description": "test_description_3", "lng": "10", "lat": "10", "rate":"1"}
    response = test_client.post(
        "/public-toilets",
        headers={"Authorization": create_test_token()},
        json=test_public_toilet_3
    )
    assert response.status_code == 400
    data = response.json()
    assert data == {'detail': 'Name already taken'}