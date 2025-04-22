import uuid
from enum import Enum

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
        
    def to_dict(self):
        """Convert the Resource object to a dictionary."""
        return {
            "resource_id": self.resource_id,
            "name": self.name,
            "resource_type": self.resource_type,
            "location": self.location,
            "status": self.status.name,  # Use the name of the ResourceStatus enum
            "assigned_incident_id": self.assigned_incident_id,
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a Resource object from a dictionary."""
        resource = cls(
            name=data["name"],
            resource_type=data["resource_type"],
            location=data["location"],
        )
        resource.resource_id = data["resource_id"]
        resource.status = ResourceStatus[data["status"]]
        resource.assigned_incident_id = data["assigned_incident_id"]
        return resource
    
