import unittest
from datetime import datetime
from app.resources.emerg_resource import Resource, ResourceStatus

class TestResource(unittest.TestCase):
    def setUp(self):
        """Set up test resources."""
        self.resource1 = Resource(name="Resource1", resource_type="Type1", location="Zone 1")
        self.resource2 = Resource(name="Resource2", resource_type="Type2", location="Zone 2", status=ResourceStatus.ASSIGNED)

    def test_resource_initialization(self):
        """Test that a Resource is initialized correctly."""
        resource = Resource(name="Resource1", resource_type="Type1", location="Zone 1")
        self.assertEqual(resource.name, "Resource1")
        self.assertEqual(resource.resource_type, "Type1")
        self.assertEqual(resource.location, "Zone 1")
        self.assertEqual(resource.status, ResourceStatus.AVAILABLE)
        self.assertIsNone(resource.assigned_incident_id)

    def test_resource_status_change(self):
        """Test that a Resource's status can be updated."""
        self.resource1.status = ResourceStatus.ASSIGNED
        self.assertEqual(self.resource1.status, ResourceStatus.ASSIGNED)

    def test_resource_to_dict(self):
        """Test serialization of a Resource object to a dictionary."""
        resource_dict = self.resource1.to_dict()
        self.assertEqual(resource_dict["name"], "Resource1")
        self.assertEqual(resource_dict["resource_type"], "Type1")
        self.assertEqual(resource_dict["location"], "Zone 1")
        self.assertEqual(resource_dict["status"], "AVAILABLE")
        self.assertIsNone(resource_dict["assigned_incident_id"])
        self.assertIn("created_at", resource_dict)
        self.assertIn("updated_at", resource_dict)

    def test_resource_from_dict(self):
        """Test deserialization of a dictionary to a Resource object."""
        resource_dict = {
            "resource_id": "12345",
            "name": "Resource1",
            "resource_type": "Type1",
            "location": "Zone 1",
            "status": "AVAILABLE",
            "assigned_incident_id": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        resource = Resource.from_dict(resource_dict)
        self.assertEqual(resource.resource_id, "12345")
        self.assertEqual(resource.name, "Resource1")
        self.assertEqual(resource.resource_type, "Type1")
        self.assertEqual(resource.location, "Zone 1")
        self.assertEqual(resource.status, ResourceStatus.AVAILABLE)
        self.assertIsNone(resource.assigned_incident_id)

if __name__ == "__main__":
    unittest.main()