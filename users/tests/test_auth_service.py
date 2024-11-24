import pytest
from services.auth_service import AuthService


def test_generate_token():
    user = {"email": "test@example.com", "role": "user"}
    token = AuthService.generate_token(user)
    assert token is not None


def test_verify_token():
    user = {"email": "test@example.com", "role": "user"}
    token = AuthService.generate_token(user)
    payload = AuthService.verify_token(token)
    assert payload['email'] == "test@example.com"
    assert payload['role'] == "user"


def test_verify_expired_token():
    import time
    user = {"email": "test@example.com", "role": "user"}
    # Generate token with a short expiration time
    token = AuthService.generate_token(user, exp_minutes=0.001)  # ~5 seconds
    time.sleep(5)  # Wait for the token to expire
    payload = AuthService.verify_token(token)
    assert payload is None
