# app.py
from flask import Flask, request
from flask_restx import Api, Resource, fields
from services.user_service import UserService
from services.destination_service import DestinationService
from services.auth_service import AuthService

app = Flask(__name__)
api = Api(
    app, version="1.0", title="Travel API", description="Travel API Microservices"
)

# Initialize services
user_service = UserService()
destination_service = DestinationService()

# Namespace definitions
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
    @api.expect(user_model)
    def post(self):
        """Authenticate user and get token"""
        try:
            data = request.json
            token = user_service.login_user(data["email"], data["password"])
            return {"token": token}, 200
        except ValueError as e:
            return {"error": str(e)}, 401


@user_ns.route("/profile")
class UserProfile(Resource):
    def get(self):
        """Get user profile"""
        token = request.headers.get("Authorization")
        if not token:
            return {"error": "Token required"}, 401

        payload = AuthService.verify_token(token)
        if not payload:
            return {"error": "Invalid or expired token"}, 401

        try:
            profile = user_service.get_user_profile(payload["email"])
            return profile, 200
        except ValueError as e:
            return {"error": str(e)}, 404


@destination_ns.route("")
class DestinationList(Resource):
    def get(self):
        """Retrieve all destinations"""
        destinations = destination_service.get_all_destinations()
        return [vars(dest) for dest in destinations], 200

    @api.expect(destination_model)
    def post(self):
        """Add a new destination (Admin only)"""
        token = request.headers.get("Authorization")
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

    app.run(debug=True)
