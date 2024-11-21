# services/user_service.py
from models.user import User
from services.auth_service import AuthService
from utils.validators import validate_email, validate_password


class UserService:
    def __init__(self):
        self.users = {}
    
    def register_user(self, name, email, password, role='User'):
        """Register a new user."""
        # Validate inputs
        if not validate_email(email):
            raise ValueError("Invalid email format")
        if not validate_password(password):
            raise ValueError("Password does not meet requirements")
        
        # Check if email already exists
        if email in self.users:
            raise ValueError("Email already registered")
        
        # Hash password
        hashed_password = AuthService.hash_password(password)
        
        # Create user
        user = User(name, email, hashed_password, role)
        self.users[email] = user
        
        return user
    
    def login_user(self, email, password):
        """Authenticate user and generate token."""
        user = self.users.get(email)
        if not user:
            raise ValueError("User not found")
        
        # Verify password
        if not AuthService.verify_password(password, user.password):
            raise ValueError("Invalid password")
        
        # Generate token
        token = AuthService.generate_token(user)
        return token
    
    def get_user_profile(self, email):
        """Retrieve user profile."""
        user = self.users.get(email)
        if not user:
            raise ValueError("User not found")
        
        return {
            'name': user.name,
            'email': user.email,
            'role': user.role
        }