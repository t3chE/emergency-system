import uuid
from enum import Enum
from datetime import datetime

class ResourceStatus(Enum):
    """Enum for resource status."""

    AVAILABLE = "available"
    ASSIGNED = "assigned"
    UNAVAILABLE = "unavailable"

    
class Resource:
    """Class representing an emergency resource."""
    
    def __init__(self, name: str, resource_type: str, location: str, status: str = "available"):
        self.resource_id = str(uuid.uuid4()) # Generate a unique ID for the resource
        self.name = name
        self.resource_type = resource_type
        self.location = location
        self.status = ResourceStatus[status.upper()]  # Convert string to ResourceStatus enum
        self.assigned_incident_id: str = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


    def __str__(self):
        return (f"Resource ID: {self.resource_id}\n"
                f"Name: {self.name}\n"
                f"Type: {self.resource_type}\n"
                f"Location: {self.location}\n"
                f"Status: {self.status.value}\n"
                f"Assigned to Incident: {self.assigned_incident_id if self.assigned_incident_id else 'None'}\n"
                f"----------------------------------\n")
        
    def to_dict(self):
        """Convert the Resource object to a dictionary."""
        return {
            "resource_id": self.resource_id,
            "name": self.name,
            "resource_type": self.resource_type,
            "location": self.location,
            "status": self.status.name,  # Use the name of the ResourceStatus enum
            "assigned_incident_id": self.assigned_incident_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a Resource object from a dictionary."""
        resource = cls(
            name=data["name"],
            resource_type=data["resource_type"],
            location=data["location"],
            status=data["status"],  # Status is passed as a string
        )
        resource.resource_id = data["resource_id"]
        resource.assigned_incident_id = data["assigned_incident_id"]
        resource.created_at = datetime.fromisoformat(data["created_at"])
        resource.updated_at = datetime.fromisoformat(data["updated_at"])
        return resource
    
