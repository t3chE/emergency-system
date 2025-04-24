import unittest
import os
from app.utils.data_persistence import (
    save_incidents_to_file,
    load_incidents_from_file,
    save_resources_to_file,
    load_resources_from_file,
)
from app.incidents.emerg_incident import Incident, IncidentStatus
from app.resources.emerg_resource import Resource, ResourceStatus
from app.priorities.emerg_priority import Priority


class TestDataPersistence(unittest.TestCase):
    def setUp(self):
        """Set up test data for incidents and resources."""
        self.test_dir = "test_data"  # Directory for test files
        os.makedirs(self.test_dir, exist_ok=True)  # Ensure the directory exists

        self.incidents = {
            "1": Incident(
                location="Zone 1",
                emergency_type="Fire",
                priority=Priority.HIGH,
                required_resources=["Resource1"],
                status=IncidentStatus.OPEN,
            ),
            "2": Incident(
                location="Zone 2",
                emergency_type="Flood",
                priority=Priority.MEDIUM,
                required_resources=["Resource2"],
                status=IncidentStatus.IN_PROGRESS,
            ),
        }
        self.resources = {
            "Resource1": Resource(
                name="Resource1",
                resource_type="Type1",
                location="Zone 1",
                status=ResourceStatus.AVAILABLE,
            ),
            "Resource2": Resource(
                name="Resource2",
                resource_type="Type2",
                location="Zone 2",
                status=ResourceStatus.ASSIGNED,
            ),
        }
        self.incidents_file = os.path.join(self.test_dir, "test_incidents.json")
        self.resources_file = os.path.join(self.test_dir, "test_resources.json")

    def test_save_and_load_incidents(self):
        """Test saving and loading incidents to/from a file."""
        # Save incidents
        save_incidents_to_file(self.incidents, self.incidents_file)

        # Load incidents
        loaded_incidents = load_incidents_from_file(self.incidents_file)

        # Assert
        self.assertEqual(len(loaded_incidents), len(self.incidents))
        self.assertEqual(loaded_incidents["1"].location, self.incidents["1"].location)
        self.assertEqual(loaded_incidents["1"].priority, self.incidents["1"].priority)
        self.assertEqual(loaded_incidents["2"].status, self.incidents["2"].status)

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
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)


if __name__ == "__main__":
    unittest.main()