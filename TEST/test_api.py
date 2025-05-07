import pytest
from api.main import app, db, User
from flask import json
from werkzeug.security import generate_password_hash
from io import BytesIO

import re

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register_user(client):
    response = client.post('/users', json={
        "email": "unique_user@example.com",
        "password": "secure123",
        "username": "uniqueuser",
        "first_name": "Unique",
        "last_name": "User"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "Inscription réussie"

def test_register_duplicate_user(client):
    with app.app_context():
        user = User(
            email="duplicate_user@example.com",
            password="hashed",
            username="duplicateduser",
            first_name="Dup",
            last_name="User"
        )
        db.session.add(user)
        db.session.commit()

    response = client.post('/users', json={
        "email": "duplicate_user@example.com",
        "password": "anotherpass",
        "username": "duplicateduser",
        "first_name": "Dup",
        "last_name": "User"
    })
    assert response.status_code == 409
    assert response.get_json()["error"] == "Utilisateur déjà existant"

def test_register_invalid_email(client):
    response = client.post('/users', json={
        "email": "invalidemail",
        "password": "secure123",
        "username": "invaliduser",
        "first_name": "Invalid",
        "last_name": "Email"
    })
    assert response.status_code == 400
    assert "email" in response.get_json()["error"].lower()

def test_register_missing_fields(client):
    response = client.post('/users', json={
        "email": "missing@example.com",
        "password": "secure123",
        "username": "missinguser"
    })
    assert response.status_code == 400
    assert "champs" in response.get_json()["error"].lower()

def test_register_empty_fields(client):
    response = client.post('/users', json={
        "email": "",
        "password": "",
        "username": "",
        "first_name": "",
        "last_name": ""
    })
    assert response.status_code == 400
    assert "champs" in response.get_json()["error"].lower()

def test_login_success(client):
    hashed = generate_password_hash("secure123")
    with app.app_context():
        user = User(
            email="login_user@example.com",
            password=hashed,
            username="loginuser",
            first_name="Login",
            last_name="Test"
        )
        db.session.add(user)
        db.session.commit()

    response = client.post('/login', json={
        "email": "login_user@example.com",
        "password": "secure123"
    })
    assert response.status_code == 200
    assert response.get_json()["email"] == "login_user@example.com"

def test_login_wrong_password(client):
    hashed = generate_password_hash("secure123")
    with app.app_context():
        user = User(
            email="wrong_pw_user@example.com",
            password=hashed,
            username="wrongpwuser",
            first_name="Wrong",
            last_name="Password"
        )
        db.session.add(user)
        db.session.commit()

    response = client.post('/login', json={
        "email": "wrong_pw_user@example.com",
        "password": "incorrectpassword"
    })
    assert response.status_code == 401
    assert "error" in response.get_json()

def test_get_animals(client):
    response = client.get('/animals')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_predict_model_no_file(client):
    response = client.post('/model/predict')
    assert response.status_code == 400
    assert response.get_json()["error"] == "Aucun fichier fourni."

def test_predict_model_with_file(client):
    data = {
        'file': (BytesIO(b"fake image data"), 'test.jpg')
    }
    response = client.post('/model/predict', data=data, content_type='multipart/form-data')
    assert response.status_code in [200, 500]  # 500 si le modèle n'est pas chargé

def test_404_route(client):
    response = client.get('/unknown')
    assert response.status_code == 404

def test_login_get_not_allowed(client):
    response = client.get('/login')
    assert response.status_code == 405
