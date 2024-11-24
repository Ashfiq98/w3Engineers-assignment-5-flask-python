# tests/test_user_service.py

import pytest
from unittest.mock import patch
from services.user_service import UserService
from services.auth_service import AuthService
import time


@pytest.fixture
def user_service():
    """Fixture to provide a UserService instance with mocked persistence."""
    with patch.object(UserService, "_load_users_from_file", return_value={}), \
         patch.object(UserService, "_save_users_to_file"):
        yield UserService()


def test_register_user(user_service):
    email = f"john{time.time()}@example.com"
    user = user_service.register_user("John Doe", email, "Password123", "user")
    assert user.email == email
    assert user.name == "John Doe"
    assert user.role == "user"


def test_register_duplicate_user(user_service):
    user_service.register_user("John Doe", "john@example.com", "Password123", "user")
    with pytest.raises(ValueError, match="Email already registered"):
        user_service.register_user("John Doe", "john@example.com", "Password123", "user")


def test_login_user(user_service):
    user_service.register_user("John Doe", "john@example.com", "Password123", "user")
    token = user_service.login_user("john@example.com", "Password123")
    payload = AuthService.verify_token(token)
    assert payload["email"] == "john@example.com"
    assert payload["role"] == "user"


def test_login_invalid_password(user_service):
    user_service.register_user("John Doe", "john@example.com", "Password123", "user")
    with pytest.raises(ValueError, match="Invalid password"):
        user_service.login_user("john@example.com", "WrongPass")


def test_login_nonexistent_user(user_service):
    with pytest.raises(ValueError, match="User not found"):
        user_service.login_user("nonexistent@example.com", "Password123")
