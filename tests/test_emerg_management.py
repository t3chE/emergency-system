import unittest
from app.utils.emerg_management import EmergencyManagement
from app.incidents.emerg_incident import Incident
from app.resources.emerg_resource import Resource, ResourceStatus
from app.priorities.emerg_priority import Priority


class TestEmergencyManagement(unittest.TestCase):

    def setUp(self):
        """ Set up a fresh instance of EmergencyManagement for each test """

        self.em = EmergencyManagement()
        self.em.resources = {
            "Resource1": Resource("Resource1", ResourceStatus.AVAILABLE, "Fire Truck"),
            "Resource2": Resource("Resource2", ResourceStatus.AVAILABLE, "Ambulance"),
        }

    def test_add_incident(self):
        """ Test adding a new incident """
        incident_id = self.em.add_incident(
            location="Zone 1",
            emergency_type="Fire",
            priority="high",
            required_resources=["Resource1"]
        )
        self.assertEqual(len(self.em.incidents), 1)
        self.assertEqual(self.em.incidents[0].incident_id, incident_id)
        self.assertEqual(self.em.incidents[0].location, "Zone 1")
        self.assertEqual(self.em.incidents[0].priority, Priority.HIGH)
        self.assertIn("Resource1", self.em.incidents[0].assigned_resources)

    def test_update_incident(self):
        """ Test updating an existing incident """
        incident_id = self.em.add_incident(
            location="Zone 1",
            emergency_type="Fire",
            priority="high",
            required_resources=["Resource1"]
        )
        updated = self.em.update_incident(
            incident_id=incident_id,
            location="Zone 2",
            emergency_type="Flood",
            priority="medium",
            required_resources=["Resource2"],
            status="IN_PROGRESS"
        )
        self.assertTrue(updated)
        incident = next(i for i in self.em.incidents if i.incident_id == incident_id)
        self.assertEqual(incident.location, "Zone 2")
        self.assertEqual(incident.emerg_type, "Flood")
        self.assertEqual(incident.priority, Priority.CATEGORY_2)
        self.assertEqual(incident.status.name, "IN_PROGRESS")
        self.assertIn("Resource2", incident.assigned_resources)

    def test_allocate_resource(self):
        """ Test allocating a resource to an incident """
        incident_id = self.em.add_incident(
            location="Zone 1",
            emergency_type="Fire",
            priority="high",
            required_resources=["Resource1"]
        )
        allocated = self.em.allocate_resource(incident_id, "Resource1")
        self.assertTrue(allocated)
        resource = self.em.resources["Resource1"]
        self.assertEqual(resource.status, ResourceStatus.ALLOCATED)
        self.assertEqual(resource.assigned_incident_id, incident_id)

    def test_reallocate_resource(self):
        """ Test reallocating a resource to another incident """
        incident_id1 = self.em.add_incident(
            location="Zone 1",
            emergency_type="Fire",
            priority="high",
            required_resources=["Resource1"]
        )
        incident_id2 = self.em.add_incident(
            location="Zone 2",
            emergency_type="Flood",
            priority="medium",
            required_resources=[]
        )
        self.em.allocate_resource(incident_id1, "Resource1")
        reallocated = self.em.reallocate_resource(incident_id2, "Resource1")
        self.assertTrue(reallocated)
        resource = self.em.resources["Resource1"]
        self.assertEqual(resource.assigned_incident_id, incident_id2)

    def test_save_and_load_data(self):
        """ Test saving and loading data """
        # Add an incident and save data
        self.em.add_incident(
            location="Zone 1",
            emergency_type="Fire",
            priority="high",
            required_resources=["Resource1"]
        )
        self.em.save_data("test_incidents.json", "test_resources.json")

        # Create a new instance and load data
        new_em = EmergencyManagement()
        new_em.load_data("test_incidents.json", "test_resources.json")

        self.assertEqual(len(new_em.incidents), 1)
        self.assertEqual(len(new_em.resources), 2)
        self.assertEqual(new_em.incidents[0].location, "Zone 1")

    def tearDown(self):
        """ Clean up after each test """
        import os
        if os.path.exists("test_incidents.json"):
            os.remove("test_incidents.json")
        if os.path.exists("test_resources.json"):
            os.remove("test_resources.json")


if __name__ == "__main__":
    unittest.main()