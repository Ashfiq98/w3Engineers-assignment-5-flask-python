import json
from models.user import User
from services.auth_service import AuthService
from utils.validators import validate_email, validate_password


class UserService:
    def __init__(self, users_file='users.json'):
        self.users_file = users_file
        self.users = self.load_users_from_file()

    def load_users_from_file(self):
        """Load users from the JSON file."""
        try:
            with open(self.users_file, 'r') as f:
                users_data = json.load(f)
                # Convert raw user data into User objects
                users = {}
                for email, user_data in users_data.items():
                    users[email] = User(user_data['name'], user_data['email'], user_data['password'], user_data['role'])
                return users
        except FileNotFoundError:
            return {}  # Return an empty dictionary if the file doesn't exist
        except json.JSONDecodeError:
            raise ValueError("Error decoding the users file")

    def save_users_to_file(self):
        """Save current users to the JSON file."""
        users_data = {}
        for email, user in self.users.items():
            users_data[email] = {
                'name': user.name,
                'email': user.email,
                'password': user.password,
                'role': user.role
            }

        with open(self.users_file, 'w') as f:
            json.dump(users_data, f, indent=4)

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

        # Save updated users to file
        self.save_users_to_file()

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
