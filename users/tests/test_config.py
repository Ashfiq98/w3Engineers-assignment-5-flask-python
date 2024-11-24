# tests/test_config.py

class TestConfig:
    TESTING = True
    SECRET_KEY = "test_secret"
    JWT_SECRET_KEY = "test_jwt_secret"
    ADMIN_SECRET = "test_admin_secret"
    DEBUG = False
    ENV = "testing"
