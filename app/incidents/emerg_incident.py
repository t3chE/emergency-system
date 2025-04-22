import uuid
from app.priorities.emerg_priority import Priority # Import Priority for priority levels
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

    def __init__(self, location, emergency_type, priority, required_resources):
        self.location = location
        self.emerg_type = emergency_type
        try:
            self.priority = Priority[priority.upper()]
        except KeyError:
            raise ValueError(f"Invalid priority: {priority}. Must be one of {list(Priority.__members__.keys())}.")    
        self.required_resources = required_resources
        self.assigned_resources = []
        self.status = IncidentStatus.OPEN 
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

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
        