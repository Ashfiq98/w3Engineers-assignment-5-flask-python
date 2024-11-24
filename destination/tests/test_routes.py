import pytest
from app import app
from services.auth_service import AuthService


@pytest.fixture
def preload_destination():
    # Preload destinations into the service for testing
    from services.destination_service import DestinationService
    service = DestinationService()
    destination = service.add_destination('Preloaded', 'For Testing', 'Location')
    return destination  # Return the created destination


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_admin_token():
    # Mock an admin token
    user = type("User", (), {"email": "admin@admin.com", "role": "admin"})
    return AuthService.generate_token(user)


@pytest.fixture
def mock_user_token():
    # Mock a non-admin user token
    user = type("User", (), {"email": "user@user.com", "role": "user"})
    return AuthService.generate_token(user)


def test_get_destinations(client):
    response = client.get('/destinations')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_post_destination_without_token(client):
    response = client.post('/destinations', json={
        'name': 'New York',
        'description': 'Big Apple',
        'location': 'USA'
    })
    assert response.status_code == 401
    assert response.json['error'] == 'Token required'


def test_post_destination_with_invalid_token(client, mock_user_token):
    response = client.post('/destinations', json={
        'name': 'New York',
        'description': 'Big Apple',
        'location': 'USA'
    }, headers={'Authorization': f'{mock_user_token}'})
    assert response.status_code == 403
    assert response.json['error'] == 'Admin access required'


def test_post_destination_with_valid_token(client, mock_admin_token):
    response = client.post('/destinations', json={
        'name': 'New York',
        'description': 'Big Apple',
        'location': 'USA'
    }, headers={'Authorization': f'{mock_admin_token}'})
    assert response.status_code == 201
    assert response.json['name'] == 'New York'


def test_delete_destination_without_token(client):
    response = client.delete('/destinations/1')
    assert response.status_code == 401
    assert response.json['error'] == 'Please! authorize with token first..'


def test_delete_destination_with_invalid_token(client, mock_user_token):
    response = client.delete('/destinations/1', headers={'Authorization': f'{mock_user_token}'})
    assert response.status_code == 403
    assert response.json['error'] == 'Admin access required.'


def test_delete_destination_with_valid_token(client, mock_admin_token, preload_destination):
    destination_id = preload_destination.id  # Get the ID of the preloaded destination
    response = client.delete(f'/destinations/{destination_id}', headers={'Authorization': f'{mock_admin_token}'})
    assert response.status_code == 200
    assert response.json['message'] == 'Destination deleted successfully'
