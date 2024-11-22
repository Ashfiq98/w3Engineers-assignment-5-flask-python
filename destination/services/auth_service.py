# services/auth_service.py
import jwt
import datetime
import bcrypt
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class AuthService:
    # Load the secret key from the environment variable
    SECRET_KEY = os.getenv('JWT_Secret_Key', 'fallback_secret')  # Fallback for safety during testing

    @staticmethod
    def generate_token(user):
        """
        Generate JWT token for the user.
        :param user: An object or dict with 'email' and 'role' attributes
        """
        payload = {
            'email': user.email,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        return jwt.encode(payload, AuthService.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_token(token):
        """
        Verify and decode JWT token.
        :param token: The JWT token to verify
        :return: Decoded payload if valid, or None if invalid/expired
        """
        try:
            payload = jwt.decode(token, AuthService.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def hash_password(password):
        """
        Hash password using bcrypt.
        :param password: Plain text password
        :return: Hashed password
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Verify password against hashed password.
        :param plain_password: User-provided password
        :param hashed_password: Stored hashed password
        :return: Boolean indicating if the passwords match
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

    @staticmethod
    def check_admin_access(token):
        """
        Check if the provided token belongs to an admin user.
        :param token: JWT token
        :return: Boolean indicating if the user is an admin
        """
        payload = AuthService.verify_token(token)
        print(payload.get('role'))
        return payload and payload.get('role') == 'admin'
