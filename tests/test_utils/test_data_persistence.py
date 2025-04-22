import unittest
import os
from app.utils.data_persistence import (
    save_incidents_to_file,
    load_incidents_from_file,
    save_resources_to_file,
    load_resources_from_file,
)
from app.incidents.emerg_incident import Incident
from app.resources.emerg_resource import Resource, ResourceStatus

class TestDataPersistence(unittest.TestCase):
    def setUp(self):
        """Set up test data for incidents and resources."""
        self.incidents = [
            Incident("Zone 1", "Fire", "high", ["Resource1"]),
            Incident("Zone 2", "Flood", "medium", ["Resource2"]),
        ]
        self.resources = {
            "Resource1": Resource("Resource1", ResourceStatus.AVAILABLE, "Zone 1"),
            "Resource2": Resource("Resource2", ResourceStatus.ASSIGNED, "Zone 2"),
        }
        self.incidents_file = "test_incidents.json"
        self.resources_file = "test_resources.json"

    def test_save_and_load_incidents(self):
        """Test saving and loading incidents to/from a file."""
        # Save incidents
        save_incidents_to_file(self.incidents, self.incidents_file)

        # Load incidents
        loaded_incidents = load_incidents_from_file(self.incidents_file)

        # Assert
        self.assertEqual(len(loaded_incidents), len(self.incidents))
        self.assertEqual(loaded_incidents[0].location, self.incidents[0].location)
        self.assertEqual(loaded_incidents[1].priority, self.incidents[1].priority)

    def test_save_and_load_resources(self):
        """Test saving and loading resources to/from a file."""
        # Save resources
        save_resources_to_file(self.resources, self.resources_file)

        # Load resources
        loaded_resources = load_resources_from_file(self.resources_file)

        # Assert
        self.assertEqual(len(loaded_resources), len(self.resources))
        self.assertEqual(loaded_resources["Resource1"].status, self.resources["Resource1"].status)
        self.assertEqual(loaded_resources["Resource2"].location, self.resources["Resource2"].location)

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.incidents_file):
            os.remove(self.incidents_file)
        if os.path.exists(self.resources_file):
            os.remove(self.resources_file)

if __name__ == "__main__":
    unittest.main()