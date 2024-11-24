# tests/test_routes.py

import pytest
from unittest.mock import patch
from app import create_app
from tests.test_config import TestConfig
from services.user_service import UserService
import time


@pytest.fixture
def client():
    app = create_app(TestConfig)

    # Reset user data here
    with patch.object(UserService, "_load_users_from_file", return_value={}), \
         patch.object(UserService, "_save_users_to_file"):
        user_service = UserService()
        user_service.users = {}  # Clear existing users for tests

        with app.test_client() as client:
            yield client


def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "name": "Test User",
            "email": f"test{time.time()}@example.com",
            "password": "TestPass123",
            "role": "user",
        },
    )
    print("Response status code:", response.status_code)
    print("Response data:", response.json)
    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully"


def test_register_duplicate_user(client):
    email = f"duplicate{time.time()}@example.com"
    client.post(
        "/users/register",
        json={
            "name": "Duplicate User",
            "email": email,
            "password": "TestPass123",
            "role": "user",
        },
    )
    response = client.post(
        "/users/register",
        json={
            "name": "Duplicate User",
            "email": email,
            "password": "TestPass123",
            "role": "user",
        },
    )
    print("Response status code:", response.status_code)
    print("Response data:", response.json)
    assert response.status_code == 400
    assert response.json["error"] == "Email already registered"


def test_login_user(client):
    email = f"login{time.time()}@example.com"
    client.post(
        "/users/register",
        json={
            "name": "Login User",
            "email": email,
            "password": "LoginPass123",
            "role": "user",
        },
    )
    response = client.post(
        "/users/login",
        json={"email": email, "password": "LoginPass123"},
    )
    print("Response status code:", response.status_code)
    print("Response data:", response.json)
    assert response.status_code == 200
    assert "token" in response.json


def test_login_invalid_password(client):
    email = f"invalidpass{time.time()}@example.com"
    client.post(
        "/users/register",
        json={
            "name": "Invalid Password User",
            "email": email,
            "password": "ValidPass123",
            "role": "user",
        },
    )
    response = client.post(
        "/users/login",
        json={"email": email, "password": "WrongPass"},
    )
    print("Response status code:", response.status_code)
    print("Response data:", response.json)
    assert response.status_code == 401
    assert response.json["error"] == "Invalid password"


def test_register_missing_fields(client):
    response = client.post(
        "/users/register",
        json={"name": "Incomplete User"},  # Missing required fields
    )
    assert response.status_code == 400
    assert "error" in response.json


def test_register_invalid_role(client):
    response = client.post(
        "/users/register",
        json={
            "name": "Invalid Role User",
            "email": "invalidrole@example.com",
            "password": "Password123",
            "role": "invalid_role",
        },
    )
    assert response.status_code == 400
    assert response.json["error"] == "Invalid role specified"


def test_register_admin_with_invalid_token(client):
    response = client.post(
        "/users/register",
        json={
            "name": "Admin User",
            "email": "adminuser@example.com",
            "password": "AdminPass123",
            "role": "admin",
            "admin_token": "wrong_token",
        },
    )
    assert response.status_code == 403
    assert response.json["error"] == "Invalid admin token"


def test_login_nonexistent_user(client):
    response = client.post(
        "/users/login",
        json={"email": "nonexistent@example.com", "password": "Password123"},
    )
    assert response.status_code == 401
    assert response.json["error"] == "User not found"


def test_login_wrong_password(client):
    email = f"wrongpass{time.time()}@example.com"
    client.post(
        "/users/register",
        json={
            "name": "Wrong Password User",
            "email": email,
            "password": "CorrectPass123",
            "role": "user",
        },
    )
    response = client.post(
        "/users/login",
        json={"email": email, "password": "WrongPass"},
    )
    assert response.status_code == 401
    assert response.json["error"] == "Invalid password"


def test_profile_no_token(client):
    response = client.get("/users/profile")
    assert response.status_code == 401
    assert response.json["error"] == "Authorization token required (format: <token>)"


def test_profile_invalid_token(client):
    response = client.get(
        "/users/profile", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert response.json["error"] == "Invalid or expired token"