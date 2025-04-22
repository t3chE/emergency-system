import uuid
from enum import Enum
from datetime import datetime
from typing import Optional

class ResourceStatus(Enum):
    """Enum for resource status."""
    AVAILABLE = "available"
    ASSIGNED = "assigned"
    UNAVAILABLE = "unavailable"

    def __str__(self):  # Added for consistent string representation
        return self.value
    
    def __repr__(self):
        return f"<{self.__class__.__name__}.{self.name}: {self.value}>"

class Resource:
    """Class representing an emergency resource."""

    def __init__(self,
                 name: str,
                 resource_type: str,
                 location: str,
                 status: ResourceStatus = ResourceStatus.AVAILABLE,  # Use Enum as default
                 resource_id: Optional[str] = None,
                 assigned_incident_id: Optional[str] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        """
        Initializes a Resource object.

        Args:
            name (str): The name of the resource.
            resource_type (str): The type of resource (e.g., "Ambulance", "Fire Truck").
            location (str): The location of the resource.
            status (ResourceStatus, optional): The status of the resource.
                Defaults to ResourceStatus.AVAILABLE.
            resource_id (Optional[str], optional): The unique ID of the resource.
                Defaults to None, which generates a new ID.
            assigned_incident_id (Optional[str], optional): The ID of the incident
                this resource is assigned to. Defaults to None.
            created_at (Optional[datetime], optional): The creation timestamp.
                Defaults to None, which uses the current time.
            updated_at (Optional[datetime], optional): The last update timestamp.
                Defaults to None, which uses the current time.
        """
        self.resource_id = resource_id if resource_id else str(uuid.uuid4())
        self.name = name
        self.resource_type = resource_type
        self.location = location
        self.status = status
        self.assigned_incident_id = assigned_incident_id
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()
        self._validate_inputs()

    def _validate_inputs(self):
        """Validates the input arguments."""
        if not isinstance(self.name, str):
            raise ValueError("Name must be a string.")
        if not isinstance(self.resource_type, str):
            raise ValueError("Resource type must be a string.")
        if not isinstance(self.location, str):
            raise ValueError("Location must be a string.")
        if not isinstance(self.status, ResourceStatus):
            raise ValueError(f"Status must be an instance of ResourceStatus Enum, got {type(self.status)}.")
        if self.assigned_incident_id and not isinstance(self.assigned_incident_id, str):
            raise ValueError("assigned_incident_id must be a string or None.")
        if not isinstance(self.created_at, datetime):
            raise ValueError("created_at must be a datetime object.")
        if not isinstance(self.updated_at, datetime):
            raise ValueError("updated_at must be a datetime object.")

    def __str__(self) -> str:
        """Returns a user-friendly string representation of the resource."""
        return (f"Resource ID: {self.resource_id}\n"
                f"Name: {self.name}\n"
                f"Type: {self.resource_type}\n"
                f"Location: {self.location}\n"
                f"Status: {self.status}\n"  # Use the Enum's __str__
                f"Assigned to Incident: {self.assigned_incident_id or 'None'}\n"
                f"Created At: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Updated At: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def __repr__(self) -> str:
        """Official string representation for developers (useful for debugging)."""
        return (f"Resource(resource_id='{self.resource_id}', name='{self.name}', "
                f"resource_type='{self.resource_type}', location='{self.location}', "
                f"status={self.status}, assigned_incident_id='{self.assigned_incident_id}', "
                f"created_at={self.created_at}, updated_at={self.updated_at})")

    def to_dict(self) -> dict:
        """Convert the Resource object to a dictionary."""
        return {
            "resource_id": self.resource_id,
            "name": self.name,
            "resource_type": self.resource_type,
            "location": self.location,
            "status": self.status.name,  # Store Enum as name
            "assigned_incident_id": self.assigned_incident_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Resource':
        """Create a Resource object from a dictionary."""
        status_str = data.get("status")
        try:
            status = ResourceStatus[status_str] if status_str else ResourceStatus.AVAILABLE
        except KeyError:
            status = ResourceStatus.AVAILABLE
        return cls(
            resource_id=data["resource_id"],
            name=data["name"],
            resource_type=data["resource_type"],
            location=data["location"],
            status=status,  # Convert string from dict to Enum
            assigned_incident_id=data.get("assigned_incident_id"),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )
    
