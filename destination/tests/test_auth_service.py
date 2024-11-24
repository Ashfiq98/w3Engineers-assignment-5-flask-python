import pytest
from services.auth_service import AuthService
import datetime
import jwt


@pytest.fixture
def valid_token():
    user = type("User", (), {"email": "user@example.com", "role": "user"})
    return AuthService.generate_token(user)


@pytest.fixture
def expired_token():
    # Create an expired token
    user = type("User", (), {"email": "user@example.com", "role": "user"})
    payload = {
        'email': user.email,
        'role': user.role,
        'exp': datetime.datetime.utcnow() - datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, AuthService.SECRET_KEY, algorithm='HS256')


def test_generate_token(valid_token):
    assert isinstance(valid_token, str)


def test_verify_token(valid_token):
    payload = AuthService.verify_token(valid_token)
    assert payload is not None
    assert payload['email'] == "user@example.com"


def test_verify_invalid_token(expired_token):
    payload = AuthService.verify_token(expired_token)
    assert payload is None


def test_check_admin_access(valid_token):
    payload = AuthService.verify_token(valid_token)
    is_admin = AuthService.check_admin_access(valid_token)
    assert is_admin == (payload['role'] == 'admin')
