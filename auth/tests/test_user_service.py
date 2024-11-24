import pytest
from services.user_service import UserService
# from services.auth_service import AuthService


@pytest.fixture
def user_service():
    return UserService()


def test_register_user(user_service):
    user = user_service.register_user("John Doe", "john@example.com", "Password123")
    assert user.name == "John Doe"
    assert user.email == "john@example.com"


def test_register_duplicate_user(user_service):
    user_service.register_user("John Doe", "john@example.com", "Password123")
    with pytest.raises(ValueError, match="Email already registered"):
        user_service.register_user("John Doe", "john@example.com", "Password123")


def test_login_user(user_service):
    user_service.register_user("John Doe", "john@example.com", "Password123")
    token = user_service.login_user("john@example.com", "Password123")
    assert token is not None


def test_invalid_password(user_service):
    user_service.register_user("John Doe", "john@example.com", "Password123")
    with pytest.raises(ValueError, match="Invalid password"):
        user_service.login_user("john@example.com", "WrongPassword")


# def test_get_user_profile(user_service):
#     user_service.register_user("John Doe", "john@example.com", "Password123")
#     profile = user_service.get_user_profile("john@example.com")
#     assert profile['name'] == "John Doe"
#     assert profile['email'] == "john@example.com"
