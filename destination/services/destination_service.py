import os
import json
from models.destination import Destination


class DestinationService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DestinationService, cls).__new__(cls, *args, **kwargs)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.destinations = []
        self.next_id = 1

# class DestinationService:
    def __init__(self):
        # Path to the JSON file
        self.destinations_file = os.path.join(os.path.dirname(__file__), "../destinations.json")
        self.destinations = self._load_destinations_from_file()
        self.next_id = self._get_next_id()

    def _load_destinations_from_file(self):
        """Load destinations from the JSON file if it exists."""
        if os.path.exists(self.destinations_file):
            with open(self.destinations_file, "r") as file:
                data = json.load(file)
                # Convert dictionary to Destination objects
                return {int(dest_id): Destination(**details) for dest_id, details in data.items()}
        return {}

    def _save_destinations_to_file(self):
        """Save destinations to the JSON file."""
        with open(self.destinations_file, "w") as file:
            # Convert Destination objects to dictionaries
            json.dump(
                {dest_id: dest.__dict__ for dest_id, dest in self.destinations.items()},
                file,
                indent=4
            )

    def _get_next_id(self):
        """Get the next ID based on the existing destinations."""
        return max(self.destinations.keys(), default=0) + 1

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
        self._save_destinations_to_file()  # Save after adding
        return destination

    def update_destination(self, dest_id, name, description, location):
        """Replace a destination entirely."""
        if dest_id not in self.destinations:
            raise ValueError("Destination not found")

        self.destinations[dest_id] = Destination(
            id=dest_id, name=name, description=description, location=location
        )
        self._save_destinations_to_file()
        return self.destinations[dest_id]

    def partial_update_destination(self, dest_id, updates):
        """Partially update a destination."""
        if dest_id not in self.destinations:
            raise ValueError("Destination not found")

        destination = self.destinations[dest_id]
        for key, value in updates.items():
            if hasattr(destination, key):
                setattr(destination, key, value)

        self._save_destinations_to_file()
        return destination

    def get_all_destinations(self):
        """Retrieve all destinations."""
        return list(self.destinations.values())

    def delete_destination(self, dest_id):
        """Delete a specific destination."""
        if dest_id not in self.destinations:
            raise ValueError("Destination not found")

        del self.destinations[dest_id]
        self._save_destinations_to_file()  # Save after deletion
        return True