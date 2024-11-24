import pytest
from services.destination_service import DestinationService
from models.destination import Destination


@pytest.fixture
def destination_service():
    """
    Fixture to provide a clean instance of DestinationService for each test.
    This ensures test isolation.
    """
    service = DestinationService()
    # Clear any existing destinations and reset ID counter
    service.destinations = {}
    service.next_id = 1
    return service


def test_add_destination(destination_service):
    destination = destination_service.add_destination('Paris', 'City of Lights', 'France')
    assert isinstance(destination, Destination)
    assert destination.name == 'Paris'


def test_get_all_destinations(destination_service):
    # Preload data explicitly
    destination_service.add_destination('Paris', 'City of Lights', 'France')
    destination_service.add_destination('Tokyo', 'Vibrant city', 'Japan')

    destinations = destination_service.get_all_destinations()
    assert len(destinations) == 2  # Ensure we have exactly two destinations
    assert destinations[0].name == 'Paris'
    assert destinations[1].name == 'Tokyo'


def test_update_destination(destination_service):
    destination = destination_service.add_destination('New York', 'City that never sleeps', 'USA')
    updated_destination = destination_service.update_destination(destination.id, 'NYC', 'Updated Description', 'USA')
    assert updated_destination.name == 'NYC'
    assert updated_destination.description == 'Updated Description'


def test_delete_destination(destination_service):
    destination = destination_service.add_destination('Berlin', 'Historical city', 'Germany')
    result = destination_service.delete_destination(destination.id)
    assert result is True
    assert len(destination_service.get_all_destinations()) == 0  # Ensure it was deleted
