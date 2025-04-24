import unittest
from app.utils.emerg_management import EmergencyManagement
from app.incidents.emerg_incident import IncidentStatus
from app.resources.emerg_resource import Resource, ResourceStatus
from app.priorities.emerg_priority import Priority


class TestEmergencyManagement(unittest.TestCase):
    def setUp(self):
        """Set up test data for EmergencyManagement."""
        self.management = EmergencyManagement()

        # Add test incidents
        self.management.add_incident(
            incident_id="1",
            location="Zone 1",
            emergency_type="Fire",
            priority=Priority.HIGH,
            required_resources=["Resource1"],
            status=IncidentStatus.OPEN,
        )
        self.management.add_incident(
            incident_id="2",
            location="Zone 2",
            emergency_type="Flood",
            priority=Priority.MEDIUM,
            required_resources=["Resource2"],
            status=IncidentStatus.IN_PROGRESS,
        )

        # Add test resources
        self.resource1 = Resource(
            name="Resource1",
            resource_type="Type1",
            location="Zone 1",
            status=ResourceStatus.AVAILABLE,
        )
        self.resource2 = Resource(
            name="Resource2",
            resource_type="Type2",
            location="Zone 2",
            status=ResourceStatus.ASSIGNED,
        )
        self.management.add_resource("Resource1", self.resource1)
        self.management.add_resource("Resource2", self.resource2)

    def test_add_incident(self):
        """Test adding an incident to EmergencyManagement."""
        self.management.add_incident(
            incident_id="3",
            location="Zone 3",
            emergency_type="Earthquake",
            priority=Priority.LOW,
            required_resources=["Resource3"],
            status=IncidentStatus.OPEN,
        )
        self.assertIn("3", self.management.incidents)
        self.assertEqual(self.management.incidents["3"].location, "Zone 3")

    def test_add_resource(self):
        """Test adding a resource to EmergencyManagement."""
        resource = Resource(
            name="Resource3",
            resource_type="Type3",
            location="Zone 3",
            status=ResourceStatus.AVAILABLE,
        )
        self.management.add_resource("Resource3", resource)
        self.assertIn("Resource3", self.management.resources)
        self.assertEqual(self.management.resources["Resource3"].location, "Zone 3")

    def test_assign_resource_to_incident(self):
        """Test assigning a resource to an incident."""
        self.management.assign_resource_to_incident("Resource1", "1")
        self.assertEqual(self.management.resources["Resource1"].status, ResourceStatus.ASSIGNED)
        self.assertEqual(self.management.resources["Resource1"].assigned_incident_id, "1")
        self.assertIn("Resource1", self.management.incidents["1"].assigned_resources)

    def test_update_incident_status(self):
        """Test updating the status of an incident."""
        self.management.update_incident_status("1", IncidentStatus.RESOLVED)
        self.assertEqual(self.management.incidents["1"].status, IncidentStatus.RESOLVED)

    def test_update_resource_status(self):
        """Test updating the status of a resource."""
        self.management.update_resource_status("Resource1", ResourceStatus.UNAVAILABLE)
        self.assertEqual(self.management.resources["Resource1"].status, ResourceStatus.UNAVAILABLE)

    def test_get_available_resources(self):
        """Test retrieving available resources."""
        available_resources = self.management.get_available_resources()
        self.assertIn("Resource1", available_resources)
        self.assertNotIn("Resource2", available_resources)

    def test_get_open_incidents(self):
        """Test retrieving open incidents."""
        open_incidents = self.management.get_open_incidents()
        self.assertIn("1", open_incidents)
        self.assertNotIn("2", open_incidents)  # Incident 2 is IN_PROGRESS, not OPEN


if __name__ == "__main__":
    unittest.main()