import json
import os
from models.user import User
from services.auth_service import AuthService
from utils.validators import validate_email, validate_password


class UserService:
    def __init__(self):
        self.users_file = os.path.join(os.path.dirname(__file__), "../users.json")
        self.users = self._load_users_from_file()

    def _load_users_from_file(self):
        """Load users from the JSON file if it exists."""
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as file:
                data = json.load(file)
                # Convert dictionary to User objects
                return {email: User(**details) for email, details in data.items()}
        return {}

    def _save_users_to_file(self):
        """Save users to the JSON file."""
        with open(self.users_file, "w") as file:
            # Convert User objects to dictionaries
            json.dump(
                {email: user.__dict__ for email, user in self.users.items()}, file, indent=4
            )

    def register_user(self, name, email, password, role="user"):
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
        hashed_password = AuthService.hash_password(password).decode("utf-8")

        # Create a user object
        user = User(name, email, hashed_password, role)
        self.users[email] = user

        # Save to the JSON file
        self._save_users_to_file()

        return user

    def login_user(self, email, password):
        """Authenticate user and generate token."""
        user = self.users.get(email)
        if not user:
            raise ValueError("User not found")

        # Verify the password
        if not AuthService.verify_password(password, user.password.encode("utf-8")):
            raise ValueError("Invalid password")

        # Generate a JWT token
        token = AuthService.generate_token(user)
        return token

    def get_user_profile(self, email):
        """Retrieve a user's profile."""
        user = self.users.get(email)
        if not user:
            raise ValueError("User not found")

        return {
            "name": user.name,
            "email": user.email,
            "role": user.role,
        }
