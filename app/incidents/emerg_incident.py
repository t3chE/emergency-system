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
    """ This class represents an emergency incident.
    It contains attributes such as incident ID, location, emergency type,
    priority, required resources, status, assigned resources, and timestamps"""

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

    def update_status(self, new_status: IncidentStatus):
        self.status = new_status
        self.updated_at = datetime.now()

    def __repr__(self):
        return (f"Incident ID: {self.incident_id}\n"
                f"Location: {self.location}\n"
                f"Emergency Type: {self.emerg_type}\n"
                f"Priority: {self.priority}\n"
                f"Required Resources: {self.required_resources}\n"
                f"Status: {self.status.value}\n"
                f"Assigned Resources: {self.assigned_resources}\n"
                f"Created At: {self.created_at}\n"
                f"Updated At: {self.updated_at}")