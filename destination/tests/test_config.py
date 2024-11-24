import os


class Config:
    """Base configuration class."""
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'test_secret_key')


class TestConfig(Config):
    """Test-specific configuration."""
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'development'  # or 'testing'
    SECRET_KEY = 'test_secret_key'  # Use a different key for testing
    JWT_Secret_Key = 'test_jwt_secret_key'
    # You can add other test-specific configurations here (e.g., database URLs, logging levels)
