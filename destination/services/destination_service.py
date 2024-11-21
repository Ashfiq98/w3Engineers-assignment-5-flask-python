# services/destination_service.py
from models.destination import Destination


class DestinationService:
    def __init__(self):
        self.destinations = {}
        self.next_id = 1
    
    def add_destination(self, name, description, location):
        """Add a new destination."""
        destination = Destination(
            id=self.next_id,
            name=name,
            description=description,
            location=location
        )
        self.destinations[self.next_id] = destination
        self.next_id += 1
        return destination
    
    def get_all_destinations(self):
        """Retrieve all destinations."""
        return list(self.destinations.values())
    
    def delete_destination(self, dest_id):
        """Delete a specific destination."""
        if dest_id not in self.destinations:
            raise ValueError("Destination not found")
        
        del self.destinations[dest_id]
        return True