from flask import Flask, request
from flask_restx import Api, Resource, fields
from services.user_service import UserService
from services.auth_service import AuthService

app = Flask(__name__)

# Initialize Flask-RESTX API with Swagger UI enabled
api = Api(
    app,
    version="1.0",
    title="User",
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

# Namespace definitions for user and destination endpoints
user_ns = api.namespace("users", description="User operations")

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


if __name__ == "__main__":
    # Seed some initial data for testing
    app.run(debug=True, port=5003)
