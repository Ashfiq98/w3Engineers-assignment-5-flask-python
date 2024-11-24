from flask import Flask, request
from flask_restx import Api, Resource, fields
from services.destination_service import DestinationService
from services.auth_service import AuthService

app = Flask(__name__)

# Initialize Flask-RESTX API with Swagger UI enabled
api = Api(
    app,
    version="1.0",
    title="Destination",
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
destination_service = DestinationService()

destination_ns = api.namespace("destinations", description="Destination operations")

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
        if not auth_header:
            return {"error": "Token required"}, 401
        token = auth_header

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


# Destination Resource Route (For delete, update, or partial update of destinations)
@destination_ns.route("/<int:dest_id>")
class DestinationResource(Resource):
    def delete(self, dest_id):
        """Delete a destination (Admin only)"""
        token = request.headers.get("Authorization")
        if token is None:
            return {"error": "Please! authorize with token first.."}, 401
        if not AuthService.check_admin_access(token):
            return {"error": "Admin access required."}, 403

        try:
            destination_service.delete_destination(dest_id)
            return {"message": "Destination deleted successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 404

    @api.expect(destination_model)
    def put(self, dest_id):
        """Replace a destination (Admin only)"""
        token = request.headers.get("Authorization")
        if not token or not AuthService.check_admin_access(token):
            return {"error": "Admin access required"}, 403

        data = request.json
        try:
            updated_destination = destination_service.update_destination(
                dest_id, data["name"], data["description"], data["location"]
            )
            return vars(updated_destination), 200
        except ValueError as e:
            return {"error": str(e)}, 404

    @api.expect(destination_model, validate=False)
    def patch(self, dest_id):
        """Partially update a destination (Admin only)"""
        token = request.headers.get("Authorization")
        if not token or not AuthService.check_admin_access(token):
            return {"error": "Admin access required"}, 403

        data = request.json
        try:
            updated_destination = destination_service.partial_update_destination(
                dest_id, data
            )
            return vars(updated_destination), 200
        except ValueError as e:
            return {"error": str(e)}, 404


if __name__ == "__main__":
    # Load initial data from the JSON file or seed default destinations if empty
    if not destination_service.get_all_destinations():
        destination_service.add_destination('Paris', 'Beautiful city of lights', 'France')
        destination_service.add_destination('Tokyo', 'Vibrant metropolitan city', 'Japan')

    app.run(debug=True, port=5002)
