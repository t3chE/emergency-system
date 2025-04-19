import uuid
from enum import Enum

class ResourceStatus(Enum):
    AVAILABLE = "available"
    ASSIGNED = "assigned"
    UNAVAILABLE = "unavailable"

class Resource:
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
        