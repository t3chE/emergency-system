import unittest
from app.resources.emerg_resource import Resource, ResourceStatus

class TestResource(unittest.TestCase):
    def test_resource_initialization(self):
        """Test that a Resource is initialized correctly."""
        resource = Resource("Resource1", ResourceStatus.AVAILABLE, "Zone 1")
        self.assertEqual(resource.resource_id, "Resource1")
        self.assertEqual(resource.status, ResourceStatus.AVAILABLE)
        self.assertEqual(resource.location, "Zone 1")

    def test_resource_status_change(self):
        """Test that a Resource's status can be updated."""
        resource = Resource("Resource1", ResourceStatus.AVAILABLE, "Zone 1")
        resource.status = ResourceStatus.ASSIGNED
        self.assertEqual(resource.status, ResourceStatus.ASSIGNED)