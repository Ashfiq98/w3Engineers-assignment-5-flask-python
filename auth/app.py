from flask import Flask, request
from flask_restx import Api, Resource, fields
from services.user_service import UserService
app = Flask(__name__)

# Initialize Flask-RESTX API with Swagger UI enabled
api = Api(
    app,
    version="1.0",
    title="Authentication Service",
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


if __name__ == "__main__":
    # Seed some initial data for testing
    user_service.register_user(
        "Admin User", "admin@travel.com", "AdminPass123", "Admin"
    )
    user_service.register_user("Regular User", "user@travel.com", "UserPass123")
    app.run(debug=True, port=5001)
