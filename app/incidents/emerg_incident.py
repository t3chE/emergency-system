import uuid
from enum import Enum # Import Enum for status
from typing import List # Import List for type hinting
from datetime import datetime # Import datetime for timestamps

class IncidentStatus(Enum):
    """ Enum class for incident status """
    
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
    # Add more statuses as needed

class Incident:
    """ This class represents an emergency incident."""

    def __init__(self, location: str, emergency_type: str, priority, required_resources: List[str]):
        self.incident_id = str(uuid.uuid4())
        self.location = location
        self.emerg_type = emergency_type
        self.priority = priority
        self.required_resources = required_resources
        self.status = IncidentStatus.OPEN 
        self.assigned_resources: List[str] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        try:
            self.priority = Priority[priority.upper()]
        except KeyError:
            raise ValueError(f"Invalid priority level: {priority}. Must be one of {list(Priority.__members__.keys())}.")
        # Ensure priority is a valid enum member

        if not isinstance(self.priority, Priority):
            raise ValueError(f"Priority must be an instance of Priority Enum, got {type(self.priority)} instead.")
        # Ensure required_resources is a list of strings

        if not isinstance(self.required_resources, list) or not all(isinstance(res, str) for res in self.required_resources):
            raise ValueError("required_resources must be a list of strings.")
        # Ensure assigned_resources is a list of strings

        if not isinstance(self.assigned_resources, list) or not all(isinstance(res, str) for res in self.assigned_resources):
            raise ValueError("assigned_resources must be a list of strings.")
        # Ensure status is an instance of IncidentStatus Enum

        if not isinstance(self.status, IncidentStatus):
            raise ValueError(f"Status must be an instance of IncidentStatus Enum, got {type(self.status)} instead.")
        # Ensure created_at and updated_at are datetime objects     

    def update_status(self, new_status: IncidentStatus):
        self.status = new_status
        self.updated_at = datetime.now()

    def __repr__(self):
        """ String representation of the incident object """
        
        return (f"Incident ID: {self.incident_id}\n"
                f"Location: {self.location}\n"
                f"Emergency Type: {self.emerg_type}\n"
                f"Priority: {self.priority}\n"
                f"Required Resources: {self.required_resources}\n"
                f"Status: {self.status.value}\n"
                f"Assigned Resources: {self.assigned_resources}\n"
                f"Created At: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Updated At: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"----------------------------------------\n")
    
    def to_dict(self):
        """Convert the Incident object to a dictionary."""
        return {
            "incident_id": self.incident_id,
            "location": self.location,
            "emerg_type": self.emerg_type,
            "priority": self.priority.name,  # Use the name of the Priority enum
            "required_resources": self.required_resources,
            "assigned_resources": self.assigned_resources,
            "status": self.status.name,  # Use the name of the IncidentStatus enum
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Incident object from a dictionary."""
        incident = cls(
            location=data["location"],
            emergency_type=data["emerg_type"],
            priority=data["priority"],
            required_resources=data["required_resources"],
        )
        incident.incident_id = data["incident_id"]
        incident.assigned_resources = data["assigned_resources"]
        incident.status = IncidentStatus[data["status"]]
        incident.created_at = datetime.fromisoformat(data["created_at"])
        incident.updated_at = datetime.fromisoformat(data["updated_at"])
        return incident
        