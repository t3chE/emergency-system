import unittest
from app.resources.emerg_resource import Resource, ResourceStatus

class TestResource(unittest.TestCase):
    def setUp(self):
        """Set up test resources."""
        self.resource1 = Resource("Resource1", "Type1", "Zone 1")
        self.resource2 = Resource("Resource2", "Type2", "Zone 2")
        
    def test_resource_initialization(self):
        """Test that a Resource is initialized correctly."""
        resource = Resource("Resource1", "Type1", "Zone 1")
        self.assertEqual(resource.name, "Resource1")  # Check the name
        self.assertEqual(resource.resource_type, "Type1")
        self.assertEqual(resource.location, "Zone 1")
        self.assertEqual(resource.status, ResourceStatus.AVAILABLE)
        self.assertIsNone(resource.assigned_incident_id)

    def test_resource_status_change(self):
        """Test that a Resource's status can be updated."""
        resource = Resource("Resource1", "Type1", "Zone 1")
        resource.status = ResourceStatus.ASSIGNED
        self.assertEqual(resource.status, ResourceStatus.ASSIGNED)

if __name__ == "__main__":
    unittest.main()