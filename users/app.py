from flask import Flask, request
from flask_restx import Api, Resource, fields
from services.user_service import UserService
from services.auth_service import AuthService
from dotenv import load_dotenv
import os


def create_app(config=None):
    # Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)

    # Apply default configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "default_secret"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "default_jwt_secret"),
        ADMIN_SECRET=123,
        # os.getenv("ADMIN_SECRET", "default_admin_secret")
    )

    # Apply custom configuration if provided
    if config:
        app.config.from_object(config)

    # Initialize Flask-RESTX API with Swagger UI enabled
    api = Api(
        app,
        version="1.0",
        title="Users Service",
        description="Travel API Microservices",
        doc="/swagger",  # Custom Swagger UI endpoint
        security="BearerAuth",  # Add security definitions
    )

    # Define the security schema
    api.authorizations = {
        "BearerAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Bearer token used for authorization",
        }
    }

    # Initialize services
    user_service = UserService()

    # Namespace definitions for user and destination endpoints
    user_ns = api.namespace("users", description="")

    # Models for input validation
    user_model = api.model(
        "User",
        {
            "name": fields.String(required=True, description="Full Name"),
            "email": fields.String(required=True, description="Email Address"),
            "password": fields.String(required=True, description="Password"),
            "role": fields.String(required=True, description="Role: 'user' or 'admin'"),
            "admin_token": fields.String(required=False, description="Admin Token (required for admin registration)"),
        },
    )

    login_model = api.model(
        "Login",
        {
            "email": fields.String(required=True, description="Email Address"),
            "password": fields.String(required=True, description="Password"),
        },
    )

    @user_ns.route("/register")
    class UserRegistration(Resource):
        @api.expect(user_model)
        def post(self):
            """Register a new user or admin"""
            try:
                data = request.json

                required_fields = ["name", "email", "password", "role"]
                for field in required_fields:
                    if not data.get(field):
                        return {"error": f"'{field}' is a required field"}, 400

                role = data.get("role", "user")

                if role not in ["user", "admin"]:
                    return {"error": "Invalid role specified"}, 400

                if role == "admin":
                    admin_token = data.get("admin_token")
                    if not admin_token or admin_token != app.config["ADMIN_SECRET"]:
                        return {"error": "Invalid admin token"}, 403

                user = user_service.register_user(
                    data["name"], data["email"], data["password"], role
                )
                return {"message": f"{role.capitalize()} registered successfully"}, 201
            except ValueError as e:
                return {"error": str(e)}, 400
            except Exception as e:
                return {"error": "Internal Server Error", "details": str(e)}, 500

    @user_ns.route("/login")
    class UserLogin(Resource):
        @api.expect(login_model)
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
                return {"error": "Authorization token required (format: <token>)"}, 401

            try:
                payload = AuthService.verify_token(token)
                if not payload:
                    return {"error": "Invalid or expired token"}, 401

                email = payload.get("email")
                if not email:
                    return {"error": "Email missing in token payload"}, 401

                profile = user_service.get_user_profile(email)
                return profile, 200
            except ValueError as e:
                return {"error": str(e)}, 404
            except Exception as e:
                print("Unexpected error in /profile:", e)
                return {"error": "Internal Server Error"}, 500

    @user_ns.route("/get-users")
    class GetUsers(Resource):
        @api.doc(security="BearerAuth")
        def get(self):
            """Get all users with the role 'user' (Admin only)"""
            token = request.headers.get("Authorization")
            if not token:
                return {"error": "Authorization token required (format:<token>)"}, 401

            try:
                payload = AuthService.verify_token(token)
                if not payload:
                    return {"error": "Invalid or expired token"}, 401

                if payload.get("role") != "admin":
                    return {"error": "Admin access required"}, 403

                users_data = user_service.users
                # print(users_data)
                users = [
                    {"email": email, "name": user.name}
                    for email, user in users_data.items()
                    if user.role == "user"
                ]
                print(users)

                return {"users": users}, 200
            except ValueError as e:
                return {"error": str(e)}, 404
            except Exception as e:
                print("Unexpected error in /get-users:", e)
                return {"error": "Internal Server Error", "details": str(e)}, 500

    api.add_namespace(user_ns)

    return app


if __name__ == "__main__":
    app = create_app()

    try:
        if not app.config["TESTING"]:
            if not UserService().get_user_profile("admin@travel.com"):
                UserService().register_user(
                    "Admin User", "admin@travel.com", "AdminPass123", "admin"
                )
    except ValueError:
        pass

    try:
        if not UserService().get_user_profile("user@travel.com"):
            UserService().register_user(
                "Regular User", "user@travel.com", "UserPass123", "user"
            )
    except ValueError:
        pass

    app.run(debug=True, port=5003)
