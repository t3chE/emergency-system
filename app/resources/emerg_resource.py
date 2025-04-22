import uuid
from enum import Enum
from app.utils.emerg_management import EmergencyManagement

class ResourceStatus(Enum):
    """Enum for resource status."""

    AVAILABLE = "available"
    ASSIGNED = "assigned"
    UNAVAILABLE = "unavailable"

class Resource:
    """Class representing an emergency resource."""
    
    def __init__(self, name: str, resource_type: str, location: str):
        self.resource_id = str(uuid.uuid4())
        self.name = name
        self.resource_type = resource_type
        self.location = location
        self.status = ResourceStatus.AVAILABLE
        self.assigned_incident_id: str = None

        def __str__(self):
            return (f"Resource ID: {self.resource_id}\n"
                    f"Name: {self.name}\n"
                    f"Type: {self.resource_type}\n"
                    f"Location: {self.location}\n"
                    f"Status: {self.status.value}\n"
                    f"Assigned to Incident: {self.assigned_incident_id if self.assigned_incident_id else 'None'}\n"
                    f"----------------------------------\n"
                     ) 
        
        def setUp(self):
            """ Set up a fresh instance of EmergencyManagement for each test """
            self.em = EmergencyManagement()
            self.em.resources = {
                "Resource1": Resource("Resource1", ResourceStatus.AVAILABLE, "Zone 1"),
                "Resource2": Resource("Resource2", ResourceStatus.AVAILABLE, "Zone 2"),
        }
        