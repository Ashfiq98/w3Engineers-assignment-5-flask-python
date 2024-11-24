# Travel API with Microservices

A Flask-based Travel API system implementing a microservices architecture with role-based authentication, destination management, and user handling capabilities.

## Features

- **Authentication Service** (Port 5001)
  - Role-based access control
  - Token-based authentication
  - Special admin authentication with secret key

- **Destination Service** (Port 5002)
  - View all destinations
  - Create new destinations (Admin only)
  - Update destination details (Admin only)
  - Delete destinations (Admin only)

- **User Service** (Port 5003)
  - User registration and login
  - Profile management
  - View all users (Admin only)

## Prerequisites

- Python 3.x
- Flask
- pytest (for running tests)

## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/Ashfiq98/w3Engineers-assignment-5-flask-python.git
```
```bash
cd w3Engineers-assignment-5-flask-python
```

2. Set up virtual environment (recommended):
```bash
python -m venv venv
```
```bash
source venv/bin/activate  # For Unix/macOS
```
```bash
venv\Scripts\activate     # For Windows
```

3. Install dependencies:

```bash
cd auth
pip install -r requirements.txt
```
```bash
cd destination
pip install -r requirements.txt
```
```bash
cd users
pip install -r requirements.txt
```

## Running the Services

Start each service in a separate terminal:

1. Authentication Service:
```bash
cd auth
```
```bash
python app.py
# Access Swagger UI at http://localhost:5001/swagger
```

2. Destination Service:
```bash
cd destination
```
```bash
python app.py
# Access Swagger UI at http://localhost:5002/swagger
```

3. User Service:
```bash
cd users
```
```bash
python app.py
# Access Swagger UI at http://localhost:5003/swagger
```

## Testing

Each microservice has its own test suite located in its respective `tests` folder. To run tests:

```bash
# Run tests for Authentication Service
cd auth
```
```bash
pytest tests/
```
```bash
# Run tests for Destination Service
cd destination
```
```bash
pytest tests/
```
```bash
# Run tests for User Service
cd users
```
```bash
pytest tests/
```

## Default User Credentials

### Admin User
- Email: admin@travel.com
- Password: AdminPass123
- Note: Admin registration requires secret key: "123"

### Regular User
- Email: user@travel.com
- Password: UserPass123

## API Documentation

Each service exposes its own Swagger UI documentation:

- Authentication Service: http://localhost:5001/swagger
- Destination Service: http://localhost:5002/swagger
- User Service: http://localhost:5003/swagger

## Service Endpoints Overview

### Authentication Service (Port 5001)
- Handles token generation and validation
- Manages role-based access control

### Destination Service (Port 5002)
- GET /destinations - List all destinations
- POST /destinations - Create new destination (Admin only)
- PUT /destinations/<id> - Update destination (Admin only)
- DELETE /destinations/<id> - Delete destination (Admin only)

### User Service (Port 5003)
- POST /register - Register new user
- POST /login - User login
- GET /profile - View user profile
- GET /users - List all users (Admin only)

## Security Features

- Role-based access control (RBAC)
- Admin registration requires secret key
- Token-based authentication
- Password hashing for security

## Code Coverage

The project maintains a minimum of 70% code coverage through comprehensive test suites.

## Author

Md. Ashfiqul Alam Chowdhury (Software Engineer - W3Engineers Ltd.)