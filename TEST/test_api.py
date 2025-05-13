
import pytest
from flask import session
from api.main import app, db, User
import json
import random

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register_user(client):
    username = f"testuser{random.randint(1000,9999)}"
    response = client.post('/users', json={
        "username": username,
        "email": f"{username}@example.com",
        "password": "securepass",
        "first_name": "Test",
        "last_name": "User"
    })
    assert response.status_code == 201


def test_login_user(client):
    client.post('/users', json={
        "username": "loginuser",
        "email": "login@example.com",
        "password": "mypassword"
    })
    response = client.post('/login', json={
        "email": "login@example.com",
        "password": "mypassword"
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'access_token' in json_data
    assert json_data['username'] == "loginuser"


def test_update_user_with_session(client):
    reg = client.post('/users', json={
        "username": "moduser",
        "email": "mod@example.com",
        "password": "password"
    })
    login_res = client.post('/login', json={
        "email": "mod@example.com",
        "password": "password"
    })
    data = login_res.get_json()
    user_id = data['id']
    token = data['access_token']

    response = client.put(f'/users/{user_id}',
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "updateduser"}
    )
    assert response.status_code == 200
    assert response.get_json()['message'] == "Utilisateur mis à jour"

def test_get_user_photos_unauthorized(client):
    response = client.get('/photos/user')
    assert response.status_code == 403

def test_get_user_photos_authorized(client):
    client.post('/users', json={
        "username": "photouser",
        "email": "photo@example.com",
        "password": "pass123"
    })
    login_res = client.post('/login', json={
        "email": "photo@example.com",
        "password": "pass123"
    })
    user_id = json.loads(login_res.data).get('id')

    with client.session_transaction() as sess:
        sess['user_id'] = user_id

    response = client.get('/photos/user')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)
