import unittest
from datetime import datetime
from app.incidents.emerg_incident import Incident, IncidentStatus
from app.priorities.emerg_priority import Priority


class TestIncident(unittest.TestCase):
    def setUp(self):
        """Set up test data for Incident tests."""
        self.location = "Zone 1"
        self.emergency_type = "Fire"
        self.priority = Priority.HIGH
        self.required_resources = ["Fire Truck", "Ambulance"]
        self.assigned_resources = ["Fire Truck"]
        self.status = IncidentStatus.IN_PROGRESS
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        self.incident = Incident(
            location=self.location,
            emergency_type=self.emergency_type,
            priority=self.priority,
            required_resources=self.required_resources,
            status=self.status,
            assigned_resources=self.assigned_resources,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def test_initialization(self):
        """Test that the Incident object is initialized correctly."""
        self.assertEqual(self.incident.location, self.location)
        self.assertEqual(self.incident.emerg_type, self.emergency_type)
        self.assertEqual(self.incident.priority, self.priority)
        self.assertEqual(self.incident.required_resources, self.required_resources)
        self.assertEqual(self.incident.status, self.status)
        self.assertEqual(self.incident.assigned_resources, self.assigned_resources)
        self.assertEqual(self.incident.created_at, self.created_at)
        self.assertEqual(self.incident.updated_at, self.updated_at)

    def test_validation(self):
        """Test input validation for the Incident class."""
        with self.assertRaises(ValueError):
            Incident(location=123, emergency_type=self.emergency_type, priority=self.priority, required_resources=self.required_resources)
        with self.assertRaises(ValueError):
            Incident(location=self.location, emergency_type=123, priority=self.priority, required_resources=self.required_resources)
        with self.assertRaises(ValueError):
            Incident(location=self.location, emergency_type=self.emergency_type, priority="INVALID_PRIORITY", required_resources=self.required_resources)
        with self.assertRaises(ValueError):
            Incident(location=self.location, emergency_type=self.emergency_type, priority=self.priority, required_resources="Not a list")
        with self.assertRaises(ValueError):
            Incident(location=self.location, emergency_type=self.emergency_type, priority=self.priority, required_resources=self.required_resources, status="INVALID_STATUS")

    def test_update_status(self):
        """Test updating the status of an Incident."""
        new_status = IncidentStatus.RESOLVED
        self.incident.update_status(new_status)
        self.assertEqual(self.incident.status, new_status)
        self.assertNotEqual(self.incident.updated_at, self.created_at)  # Ensure updated_at is changed

    def test_to_dict(self):
        """Test serialization of an Incident object to a dictionary."""
        incident_dict = self.incident.to_dict()
        self.assertEqual(incident_dict["location"], self.location)
        self.assertEqual(incident_dict["emerg_type"], self.emergency_type)
        self.assertEqual(incident_dict["priority"], self.priority.name)
        self.assertEqual(incident_dict["required_resources"], self.required_resources)
        self.assertEqual(incident_dict["assigned_resources"], self.assigned_resources)
        self.assertEqual(incident_dict["status"], self.status.name)
        self.assertEqual(incident_dict["created_at"], self.created_at.isoformat())
        self.assertEqual(incident_dict["updated_at"], self.updated_at.isoformat())

    def test_from_dict(self):
        """Test deserialization of a dictionary to an Incident object."""
        incident_dict = {
            "incident_id": "12345",
            "location": self.location,
            "emerg_type": self.emergency_type,
            "priority": self.priority.name,
            "required_resources": self.required_resources,
            "assigned_resources": self.assigned_resources,
            "status": self.status.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        incident = Incident.from_dict(incident_dict)
        self.assertEqual(incident.incident_id, "12345")
        self.assertEqual(incident.location, self.location)
        self.assertEqual(incident.emerg_type, self.emergency_type)
        self.assertEqual(incident.priority, self.priority)
        self.assertEqual(incident.required_resources, self.required_resources)
        self.assertEqual(incident.assigned_resources, self.assigned_resources)
        self.assertEqual(incident.status, self.status)
        self.assertEqual(incident.created_at, self.created_at)
        self.assertEqual(incident.updated_at, self.updated_at)


if __name__ == "__main__":
    unittest.main()