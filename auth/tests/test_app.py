# import unittest
# from unittest.mock import patch, mock_open, MagicMock
# import json
# import jwt
# import bcrypt
# from datetime import datetime, timedelta
# from services.destination_service import DestinationService
# from services.auth_service import AuthService
# from services.user_service import UserService
# # from models.destination import Destination
# # from models.user import User


# class TestUserService(unittest.TestCase):
#     def setUp(self):
#         # Mock users data - convert hashed password to string for JSON serialization
#         hashed = bcrypt.hashpw("TestPassword123!".encode('utf-8'), bcrypt.gensalt())
#         self.mock_users = {
#             "test@example.com": {
#                 "name": "Test User",
#                 "email": "test@example.com",
#                 "password": hashed.decode('utf-8'),  # Convert bytes to string for JSON
#                 "role": "User"
#             }
#         }
        
#         # Create a mock for file operations
#         mock_file_content = json.dumps(self.mock_users)
#         self.mock_open_patcher = patch('builtins.open', mock_open(read_data=mock_file_content))
#         self.mock_file = self.mock_open_patcher.start()
        
#         # Patch the save_users_to_file method to prevent actual file writing
#         self.mock_save = patch.object(UserService, 'save_users_to_file')
#         self.mock_save.start()
        
#         # Initialize service with mocked file operations
#         self.service = UserService(users_file='test_users.json')

#         # Store the original password for testing
#         self.test_password = "TestPassword123!"

#     def tearDown(self):
#         self.mock_open_patcher.stop()
#         self.mock_save.stop()

#     def test_register_user(self):
#         # Test successful registration
#         with patch.object(UserService, 'save_users_to_file') as mock_save:
#             result = self.service.register_user(
#                 "New User",
#                 "new@example.com",
#                 "ValidPassword123!"
#             )
#             self.assertEqual(result.name, "New User")
#             self.assertEqual(result.email, "new@example.com")
#             mock_save.assert_called_once()

#         # Test registration with existing email
#         with self.assertRaises(ValueError):
#             self.service.register_user(
#                 "Test User",
#                 "test@example.com",
#                 "TestPassword123!"
#             )

#         # Test registration with invalid email
#         with self.assertRaises(ValueError):
#             self.service.register_user(
#                 "Invalid",
#                 "invalid-email",
#                 "TestPassword123!"
#             )

#         # Test registration with invalid password
#         with self.assertRaises(ValueError):
#             self.service.register_user(
#                 "Invalid",
#                 "valid@example.com",
#                 "weak"
#             )

#     def test_login_user(self):
#         # Patch AuthService methods for consistent password verification
#         with patch('services.auth_service.AuthService.verify_password') as mock_verify:
#             with patch('services.auth_service.AuthService.generate_token') as mock_generate:
#                 # Setup mocks
#                 mock_verify.return_value = True
#                 mock_generate.return_value = "mock_token"

#                 # Test successful login
#                 token = self.service.login_user("test@example.com", self.test_password)
#                 self.assertEqual(token, "mock_token")

#                 # Test login with wrong password
#                 mock_verify.return_value = False
#                 with self.assertRaises(ValueError):
#                     self.service.login_user("test@example.com", "WrongPassword123!")

#                 # Test login with non-existent user
#                 with self.assertRaises(ValueError):
#                     self.service.login_user("nonexistent@example.com", "TestPassword123!")

#     def test_get_user_profile(self):
#         # Test getting existing user profile
#         profile = self.service.get_user_profile("test@example.com")
#         self.assertEqual(profile['name'], "Test User")
#         self.assertEqual(profile['email'], "test@example.com")
#         self.assertEqual(profile['role'], "User")

#         # Test getting non-existent user profile
#         with self.assertRaises(ValueError):
#             self.service.get_user_profile("nonexistent@example.com")

#     def test_load_users_from_file(self):
#         # Test successful loading of users
#         users = self.service.load_users_from_file()
#         self.assertIn("test@example.com", users)
#         self.assertEqual(users["test@example.com"].name, "Test User")

#         # Test handling of non-existent file
#         with patch('builtins.open', mock_open()) as mock_file:
#             mock_file.side_effect = FileNotFoundError
#             empty_users = UserService().load_users_from_file()
#             self.assertEqual(empty_users, {})

#         # Test handling of invalid JSON
#         with patch('builtins.open', mock_open(read_data="invalid json")):
#             with self.assertRaises(ValueError):
#                 UserService().load_users_from_file()

# # Keep the TestDestinationService and TestAuthService classes as they were...
# class TestDestinationService(unittest.TestCase):
#     # ... (keep the previous implementation)
#     pass

# class TestAuthService(unittest.TestCase):
#     # ... (keep the previous implementation)
#     pass

# if __name__ == '__main__':
#     unittest.main()
import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import bcrypt
from services.destination_service import DestinationService
from services.user_service import UserService
from models.destination import Destination


class TestDestinationService(unittest.TestCase):

    def setUp(self):
        """Set up the environment for testing DestinationService"""
        # Mocking file I/O operations
        self.mock_destinations = {
            1: Destination(id=1, name="Paris", description="The capital of France", location="France"),
            2: Destination(id=2, name="Tokyo", description="A bustling metropolis", location="Japan")
        }

        # Patch methods that interact with files
        self.mock_load_destinations = patch.object(DestinationService, '_load_destinations_from_file', return_value=self.mock_destinations)
        self.mock_load_destinations.start()

        self.mock_save_destinations = patch.object(DestinationService, '_save_destinations_to_file')
        self.mock_save_destinations.start()

        # Initialize the DestinationService
        self.destination_service = DestinationService()

    def tearDown(self):
        """Clean up the mocks after each test"""
        self.mock_load_destinations.stop()
        self.mock_save_destinations.stop()

    def test_add_destination(self):
        """Test adding a new destination"""
        new_destination = {
            "name": "New York",
            "description": "The city that never sleeps",
            "location": "USA"
        }

        # Add the destination
        added_dest = self.destination_service.add_destination(**new_destination)

        # Check the added destination details
        self.assertEqual(added_dest.name, "New York")
        self.assertEqual(added_dest.description, "The city that never sleeps")
        self.assertEqual(added_dest.location, "USA")

        # Check that the destination is saved to the file
        self.mock_save_destinations.assert_called_once()

        # Check that the new destination has the next available ID
        self.assertEqual(added_dest.id, 3)

    def test_update_destination(self):
        """Test updating an existing destination"""
        updated_data = {
            "name": "Paris",
            "description": "Updated description of Paris",
            "location": "Updated France"
        }

        # Update an existing destination
        updated_dest = self.destination_service.update_destination(1, **updated_data)

        # Check the updated destination details
        self.assertEqual(updated_dest.name, "Paris")
        self.assertEqual(updated_dest.description, "Updated description of Paris")
        self.assertEqual(updated_dest.location, "Updated France")

        # Check that the save method is called
        self.mock_save_destinations.assert_called_once()

        # Try updating a non-existent destination
        with self.assertRaises(ValueError):
            self.destination_service.update_destination(999, **updated_data)

    def test_partial_update_destination(self):
        """Test partial update of a destination"""
        partial_update = {
            "description": "New description for Tokyo"
        }

        # Partially update an existing destination
        updated_dest = self.destination_service.partial_update_destination(2, partial_update)

        # Check the partial update
        self.assertEqual(updated_dest.description, "New description for Tokyo")

        # Check that the save method is called
        self.mock_save_destinations.assert_called_once()

        # Try updating a non-existent destination
        with self.assertRaises(ValueError):
            self.destination_service.partial_update_destination(999, partial_update)

    def test_get_all_destinations(self):
        """Test retrieving all destinations"""
        destinations = self.destination_service.get_all_destinations()

        # There should be 2 destinations in the mock data
        self.assertEqual(len(destinations), 2)
        self.assertEqual(destinations[0].name, "Paris")
        self.assertEqual(destinations[1].name, "Tokyo")

    def test_delete_destination(self):
        """Test deleting an existing destination"""
        # Delete a destination
        result = self.destination_service.delete_destination(2)
        self.assertTrue(result)

        # Check that the destination was deleted
        self.assertNotIn(2, self.destination_service.destinations)

        # Check that the save method is called after deletion
        self.mock_save_destinations.assert_called_once()

        # Try deleting a non-existent destination
        with self.assertRaises(ValueError):
            self.destination_service.delete_destination(999)

    def test_load_destinations_from_file(self):
        """Test loading destinations from file"""
        # Load destinations from the mocked file
        destinations = self.destination_service._load_destinations_from_file()
        self.assertEqual(len(destinations), 2)  # We mocked 2 destinations

    def test_save_destinations_to_file(self):
        """Test saving destinations to file"""
        with patch('builtins.open', mock_open()) as mock_file:
            self.destination_service._save_destinations_to_file()
            mock_file.assert_called_once()  # Check that the file is opened for writing
            mock_file().write.assert_called_once()  # Ensure data is written

    def test_get_next_id(self):
        """Test the next ID generation logic"""
        next_id = self.destination_service._get_next_id()
        self.assertEqual(next_id, 3)  # Since we have 2 destinations, the next ID should be 3

    def test_load_empty_destinations(self):
        """Test the case where no destinations are loaded (empty file)"""
        empty_dest_service = DestinationService()
        empty_dest_service._load_destinations_from_file = MagicMock(return_value={})
        empty_dest_service._load_destinations_from_file()
        self.assertEqual(len(empty_dest_service.destinations), 0)


class TestUserService(unittest.TestCase):
    def setUp(self):
        # Mock users data - convert hashed password to string for JSON serialization
        hashed = bcrypt.hashpw("TestPassword123!".encode('utf-8'), bcrypt.gensalt())
        self.mock_users = {
            "test@example.com": {
                "name": "Test User",
                "email": "test@example.com",
                "password": hashed.decode('utf-8'),  # Convert bytes to string for JSON
                "role": "User"
            }
        }

        # Create a mock for file operations
        mock_file_content = json.dumps(self.mock_users)
        self.mock_open_patcher = patch('builtins.open', mock_open(read_data=mock_file_content))
        self.mock_file = self.mock_open_patcher.start()

        # Patch the save_users_to_file method to prevent actual file writing
        self.mock_save = patch.object(UserService, 'save_users_to_file')
        self.mock_save.start()

        # Initialize service with mocked file operations
        self.service = UserService(users_file='test_users.json')

        # Store the original password for testing
        self.test_password = "TestPassword123!"

    def tearDown(self):
        self.mock_open_patcher.stop()
        self.mock_save.stop()

    def test_register_user(self):
        # Test successful registration
        with patch.object(UserService, 'save_users_to_file') as mock_save:
            result = self.service.register_user(
                "New User",
                "new@example.com",
                "ValidPassword123!"
            )
            self.assertEqual(result.name, "New User")
            self.assertEqual(result.email, "new@example.com")
            mock_save.assert_called_once()

        # Test registration with existing email
        with self.assertRaises(ValueError):
            self.service.register_user(
                "Test User",
                "test@example.com",
                "TestPassword123!"
            )

        # Test registration with invalid email
        with self.assertRaises(ValueError):
            self.service.register_user(
                "Invalid",
                "invalid-email",
                "TestPassword123!"
            )

        # Test registration with invalid password
        with self.assertRaises(ValueError):
            self.service.register_user(
                "Invalid",
                "valid@example.com",
                "weak"
            )

    def test_login_user(self):
        # Patch AuthService methods for consistent password verification
        with patch('services.auth_service.AuthService.verify_password') as mock_verify:
            with patch('services.auth_service.AuthService.generate_token') as mock_generate:
                # Setup mocks
                mock_verify.return_value = True
                mock_generate.return_value = "mock_token"

                # Test successful login
                token = self.service.login_user("test@example.com", self.test_password)
                self.assertEqual(token, "mock_token")

                # Test login with wrong password
                mock_verify.return_value = False
                with self.assertRaises(ValueError):
                    self.service.login_user("test@example.com", "WrongPassword123!")

                # Test login with non-existent user
                with self.assertRaises(ValueError):
                    self.service.login_user("nonexistent@example.com", "TestPassword123!")

    def test_get_user_profile(self):
        # Test getting existing user profile
        profile = self.service.get_user_profile("test@example.com")
        self.assertEqual(profile['name'], "Test User")
        self.assertEqual(profile['email'], "test@example.com")
        self.assertEqual(profile['role'], "User")

        # Test getting non-existent user profile
        with self.assertRaises(ValueError):
            self.service.get_user_profile("nonexistent@example.com")

    def test_load_users_from_file(self):
        # Test successful loading of users
        users = self.service.load_users_from_file()
        self.assertIn("test@example.com", users)
        self.assertEqual(users["test@example.com"].name, "Test User")

        # Test handling of non-existent file
        with patch('builtins.open', mock_open()) as mock_file:
            mock_file.side_effect = FileNotFoundError
            empty_users = UserService().load_users_from_file()
            self.assertEqual(empty_users, {})

        # Test handling invalid file format
        with patch('builtins.open', mock_open(read_data="Invalid JSON")):
            with self.assertRaises(ValueError):
                self.service.load_users_from_file()


if __name__ == '__main__':
    unittest.main()
