from flask import Flask, request
from flask_restx import Api, Resource, fields
from services.user_service import UserService
from services.destination_service import DestinationService
from services.auth_service import AuthService

app = Flask(__name__)

# Initialize Flask-RESTX API with Swagger UI enabled
api = Api(
    app,
    version="1.0",
    title="Travel API",
    description="Travel API Microservices",
    doc="/swagger",  # Custom Swagger UI endpoint
    security='BearerAuth'  # Add security definitions
)

# Define the security schema
api.authorizations = {
    'BearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Bearer token used for authorization'
    }
}

# Initialize services
user_service = UserService()
destination_service = DestinationService()

# Namespace definitions for user and destination endpoints
user_ns = api.namespace("users", description="User operations")
destination_ns = api.namespace("destinations", description="Destination operations")

# Models for input validation
user_model = api.model(
    "User",
    {
        "name": fields.String(required=True, description="Full Name"),
        "email": fields.String(required=True, description="Email Address"),
        "password": fields.String(required=True, description="Password"),
    },
)
# Model for login (only email and password)
login_model = api.model(
    "Login",
    {
        "email": fields.String(required=True, description="Email Address"),
        "password": fields.String(required=True, description="Password"),
    },
)
destination_model = api.model(
    "Destination",
    {
        "name": fields.String(required=True, description="Destination Name"),
        "description": fields.String(
            required=True, description="Destination Description"
        ),
        "location": fields.String(required=True, description="Destination Location"),
    },
)


# User Registration Route
@user_ns.route("/register")
class UserRegistration(Resource):
    @api.expect(user_model)
    def post(self):
        """Register a new user"""
        try:
            data = request.json
            user = user_service.register_user(
                data["name"], data["email"], data["password"]
            )
            return {"message": "User registered successfully"}, 201
        except ValueError as e:
            return {"error": str(e)}, 400


@user_ns.route("/login")
class UserLogin(Resource):
    @api.expect(login_model)  # Use the login_model here
    def post(self):
        """Authenticate user and get token"""
        try:
            data = request.json
            token = user_service.login_user(data["email"], data["password"])
            return {"token": token}, 200
        except ValueError as e:
            return {"error": str(e)}, 401


# User Profile Route
@user_ns.route("/profile")
class UserProfile(Resource):
    def get(self):
        """Get user profile"""
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return {"error": "Authorization token required (format: Bearer <token>)"}, 401

        token = token.split(" ")[1]  # Extract the token part

        try:
            # Verify the token
            payload = AuthService.verify_token(token)
            if not payload:
                return {"error": "Invalid or expired token"}, 401

            # Retrieve user profile using the email from the token
            email = payload.get("email")
            if not email:
                return {"error": "Email missing in token payload"}, 401

            profile = user_service.get_user_profile(email)
            return profile, 200

        except ValueError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            print("Unexpected error in /profile:", e)  # Debug log for unexpected errors
            return {"error": "Internal Server Error"}, 500


# Destination List Route
@destination_ns.route("")
class DestinationList(Resource):
    def get(self):
        """Retrieve all destinations"""
        destinations = destination_service.get_all_destinations()
        return [vars(dest) for dest in destinations], 200

    @api.expect(destination_model)
    def post(self):
        """Add a new destination (Admin only)"""
        auth_header = request.headers.get("Authorization")
        
        # If the header is missing or doesn't start with 'Bearer', return an error
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Token required"}, 401
        
        # Extract the token from the Authorization header (after 'Bearer ')
        token = auth_header.split(" ")[1]

        # Check if the admin access is valid
        if not AuthService.check_admin_access(token):
            return {"error": "Admin access required"}, 403

        try:
            data = request.json
            destination = destination_service.add_destination(
                data["name"], data["description"], data["location"]
            )
            return vars(destination), 201
        except ValueError as e:
            return {"error": str(e)}, 400


# Destination Resource Route (For deleting destinations)
@destination_ns.route("/<int:dest_id>")
class DestinationResource(Resource):
    def delete(self, dest_id):
        """Delete a destination (Admin only)"""
        token = request.headers.get("Authorization")
        if not AuthService.check_admin_access(token):
            return {"error": "Admin access required"}, 403

        try:
            destination_service.delete_destination(dest_id)
            return {"message": "Destination deleted successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 404


if __name__ == "__main__":
    # Seed some initial data for testing
    user_service.register_user(
        "Admin User", "admin@travel.com", "AdminPass123", "Admin"
    )
    user_service.register_user("Regular User", "user@travel.com", "UserPass123")

    destination_service.add_destination("Paris", "Beautiful city of lights", "France")
    destination_service.add_destination("Tokyo", "Vibrant metropolitan city", "Japan")

    app.run(debug=True, port=5002)
