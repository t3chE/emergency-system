import uuid
from enum import Enum
from typing import List, Optional
from datetime import datetime
from app.priorities.emerg_priority import Priority  

class IncidentStatus(Enum):
    """Enum class for incident status."""
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

    def __str__(self):
        return self.value  #  String representation should be the value

class Incident:
    """This class represents an emergency incident."""

    def __init__(self,
                 location: str,
                 emergency_type: str,
                 priority: Priority,  # Use the Enum directly
                 required_resources: List[str],
                 incident_id: Optional[str] = None,  # Optional for loading
                 status: IncidentStatus = IncidentStatus.OPEN, # Default value
                 assigned_resources: Optional[List[str]] = None, # Optional for loading
                 created_at: Optional[datetime] = None,  # Optional for loading
                 updated_at: Optional[datetime] = None): # Optional for loading
        """
        Initializes an Incident object.

        Args:
            location (str): The location of the incident.
            emergency_type (str): The type of emergency.
            priority (Priority): The priority of the incident (from Priority enum).
            required_resources (List[str]): A list of required resource names (strings).
            incident_id (Optional[str], optional): The unique ID of the incident.
                Defaults to None, which generates a new ID.
            status (IncidentStatus, optional): The status of the incident.
                Defaults to IncidentStatus.OPEN.
            assigned_resources (Optional[List[str]], optional):
                A list of assigned resource names. Defaults to None.
            created_at (Optional[datetime], optional): The creation timestamp.
                Defaults to None, which uses the current time.
            updated_at (Optional[datetime], optional): The last update timestamp.
                Defaults to None, which uses the current time.
        """
        self.incident_id = incident_id if incident_id else str(uuid.uuid4())
        self.location = location
        self.emerg_type = emergency_type
        self.priority = priority
        self.required_resources = required_resources
        self.status = status
        self.assigned_resources = assigned_resources if assigned_resources else []
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()

        self._validate_inputs()  #  Call validation method

    def _validate_inputs(self):
        """
        Validates the input arguments.  This method is called by the constructor.
        """
        if not isinstance(self.location, str):
            raise ValueError("Location must be a string.")
        if not isinstance(self.emerg_type, str):
            raise ValueError("Emergency type must be a string.")
        if not isinstance(self.priority, Priority):
            raise ValueError(f"Priority must be an instance of Priority Enum, got {type(self.priority)}.")
        if not isinstance(self.required_resources, list) or not all(isinstance(res, str) for res in self.required_resources):
            raise ValueError("required_resources must be a list of strings.")
        if not isinstance(self.assigned_resources, list) or not all(isinstance(res, str) for res in self.assigned_resources):
            raise ValueError("assigned_resources must be a list of strings.")
        if not isinstance(self.status, IncidentStatus):
            raise ValueError(f"Status must be an instance of IncidentStatus Enum, got {type(self.status)}.")
        if not isinstance(self.created_at, datetime):
            raise ValueError("created_at must be a datetime object.")
        if not isinstance(self.updated_at, datetime):
            raise ValueError("updated_at must be a datetime object.")

    def update_status(self, new_status: IncidentStatus) -> None:
        """
        Updates the status of the incident.

        Args:
            new_status (IncidentStatus): The new status.
        """
        if not isinstance(new_status, IncidentStatus):
            raise ValueError(f"new_status must be an instance of IncidentStatus Enum, got {type(new_status)}.")
        self.status = new_status
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        """String representation of the incident object."""
        return (f"Incident ID: {self.incident_id}\n"
                f"Location: {self.location}\n"
                f"Emergency Type: {self.emerg_type}\n"
                f"Priority: {self.priority}\n"
                f"Required Resources: {', '.join(self.required_resources)}\n" # join
                f"Status: {self.status}\n"  # Use the Enum's __str__ method
                f"Assigned Resources: {', '.join(self.assigned_resources)}\n" # join
                f"Created At: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Updated At: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"----------------------------------------\n")

    def to_dict(self) -> dict:
        """Convert the Incident object to a dictionary."""
        return {
            "incident_id": self.incident_id,
            "location": self.location,
            "emerg_type": self.emerg_type,
            "priority": self.priority.name,  # Store Enum as name
            "required_resources": self.required_resources,
            "assigned_resources": self.assigned_resources,
            "status": self.status.name,  # Store Enum as name
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Incident':
        """Create an Incident object from a dictionary."""
        return cls(
            incident_id=data["incident_id"],
            location=data.get("location", ""),  # Use .get() with defaults
            emergency_type=data.get("emerg_type", ""),
            priority=Priority[data.get("priority", "LOW")], # .get() and default
            required_resources=data.get("required_resources", []),
            status=IncidentStatus[data.get("status", "OPEN")], # .get() and default
            assigned_resources=data.get("assigned_resources", []),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )
        