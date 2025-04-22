import unittest
from app.incidents.emerg_incident import Incident
from app.priorities.emerg_priority import Priority

class TestIncident(unittest.TestCase):
    def test_incident_initialization(self):
        """Test that an Incident is initialized correctly."""
        incident = Incident("Zone 1", "Fire", "high", ["Resource1"])
        self.assertEqual(incident.location, "Zone 1")
        self.assertEqual(incident.emerg_type, "Fire")
        self.assertEqual(incident.priority, Priority.HIGH)
        self.assertEqual(incident.required_resources, ["Resource1"])
        self.assertEqual(incident.status, "OPEN")