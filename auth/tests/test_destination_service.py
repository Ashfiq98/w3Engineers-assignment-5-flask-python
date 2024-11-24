import pytest
from services.destination_service import DestinationService


@pytest.fixture
def destination_service():
    return DestinationService()


def test_add_destination(destination_service):
    destination = destination_service.add_destination("Paris", "City of Lights", "France")
    assert destination.name == "Paris"


def test_get_all_destinations(destination_service):
    destination_service.add_destination("Paris", "City of Lights", "France")
    destinations = destination_service.get_all_destinations()
    assert len(destinations) == 1


def test_delete_destination(destination_service):
    destination = destination_service.add_destination("Paris", "City of Lights", "France")
    destination_service.delete_destination(destination.id)
    assert len(destination_service.get_all_destinations()) == 0


def test_delete_nonexistent_destination(destination_service):
    with pytest.raises(ValueError, match="Destination not found"):
        destination_service.delete_destination(999)
