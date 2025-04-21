from typing import Dict, List
from app.incidents.emerg_incident import Incident, IncidentStatus
from app.resources.emerg_resource import Resource, ResourceStatus
from app.priorities.emerg_priority import Priority
from app.utils.data_persistence import (
    save_incidents_to_file,
    load_incidents_from_file,
    save_resources_to_file,
    load_resources_from_file,
)

class EmergencyManagement:
    """ Class to manage emergency incidents, resources, and priorities """

    def __init__(self):
        self.incidents: Dict[Incident] = []
        self.resources: Dict[str, Resource] = {}
        self.location_mapping = {}
        self.initialize_location_mapping()

    def save_data(self, incidents_file: str, resources_file: str):
        """ Save incidents and resources to JSON files """
        save_incidents_to_file(self.incidents, incidents_file)
        save_resources_to_file(self.resources, resources_file)

    def load_data(self, incidents_file: str, resources_file: str):
        """ Load incidents and resources from JSON files """
        self.incidents = load_incidents_from_file(incidents_file)
        self.resources = load_resources_from_file(resources_file)
        
    def initialize_location_mapping(self):
        """ Initialize the location mapping for resources """
       
        self.location_mapping = {
            "Zone 1": (51.4592, -0.2567),  # Example coordinates
            "Zone 2": (51.4761, -0.1441),
            "Zone 3": (51.4575, -0.1165),
            "Zone 4": (51.4573, -0.1437),
            "Zone 5": (51.3697, -0.0779),
            "Zone 6": (51.4882, -0.0958),
            "Zone 7": (51.4789, -0.2017),
            "Zone 8": (51.4789, -0.1221),
            "Zone 9": (51.4571, -0.0057),
            "Zone 10": (51.4695, -0.0685),
        }    

    def add_incident(self, location: str, emergency_type: str, priority: str, required_resources: List[str]):
        """ Add a new incident to the system """

        incident = Incident(location, emergency_type, priority, required_resources)
        self.incidents.append(incident)
        for resource_id in required_resources:
            resource = self.resources.get(resource_id)
            if resource:
                resource.status = ResourceStatus.ALLOCATED
                incident.assigned_resources.append(resource_id)
                resource.assigned_incident_id = incident.incident_id
        self.resources[incident.incident_id] = incident
        return incident.incident_id

    def update_incident(self, incident_id: str, location: str = None, emergency_type: str = None,
            priority: str = None, required_resources: List[str] = None, status: str = None):    
        """ Update an existing incident """

        incident = next((incident for incident in self.incidents if incident.incident_id == incident_id), None)
        if incident:
            if location:
                incident.location = location
            if emergency_type:
                incident.emerg_type = emergency_type
            if priority:
                incident.priority = priority
            if required_resources:
                incident.required_resources = required_resources
            if status:
                incident.update_status(status)
            return True
        return False
    
    def view_incidents(self) -> List[Incident]:
        """ View all incidents """
        return self.incidents

    def assign_priority(self, priority: Priority):
        self.priorities[priority.id] = priority
        
    def view_resources(self) -> List[Resource]:
        """ View all resources """
        return [resource for resource in self.resources.values() if resource.status == ResourceStatus.AVAILABLE]
    
    def allocate_resource(self, incident_id: str, resource_id: str):
        """ Allocate a resource to an incident """

        incident = next((incident for incident in self.incidents if incident.incident_id == incident_id), None)
        resource = self.resources.get(resource_id)
        if incident and resource and resource.status == ResourceStatus.AVAILABLE:
            incident.assigned_resources.append(resource_id)
            resource.assigned_incident_id = incident_id
            resource.status = ResourceStatus.ALLOCATED
            return True
        return False

    def reallocate_resource(self, incident_id: str, resource_id: str):
        """ Reallocate a resource from one incident to another """

        incident = next((incident for incident in self.incidents if incident.incident_id == incident_id), None)
        resource = self.resources.get(resource_id)
        if incident and resource and resource.status == ResourceStatus.ALLOCATED:
            resource.assigned_incident_id = incident_id
            return True
        return False

    def get_incident_report(self) -> List[Incident]:
        """ Generate a report of all incidents """
        return self.incidents
    
    def get_active_incidents(self) -> List[Incident]:
        """ Get all active incidents """
        return [incident for incident in self.incidents if incident.status == IncidentStatus.OPEN]
    
    def run(self):
        """ Run the emergency management system """
        # Sample data for testing

        while True:
            print("\n")
            print("==========================================")
            print("Welcome to the Emergency Management System")
            print("==========================================\n")
            print("1. Add Incident")
            print("2. Update Incident")
            print("3. View Incidents")
            print("4. Allocate Resource")
            print("5. Reallocate Resource")
            print("6. View Resources")
            print("7. Generate Incident Report")
            print("8. Exit\n")
            print("==========================================\n")

            choice = input("Enter your choice: ")
            if choice == '1':
                location = input("Enter location: ")
                emergency_type = input("Enter emergency type: ")
                priority = input("Enter priority: ")
                required_resources = input("Enter required resources (comma separated): ").split(',')
                self.add_incident(location, emergency_type, priority, required_resources)

            elif choice == '2':
                incident_id = input("Enter incident ID to update: ")
                location = input("Enter new location (or leave blank): ")
                emergency_type = input("Enter new emergency type (or leave blank): ")
                priority = input("Enter new priority (or leave blank): ")
                required_resources = input("Enter new required resources (comma separated or leave blank): ").split(',')
                status = input("Enter new status (or leave blank): ")
                self.update_incident(incident_id, location, emergency_type, priority, required_resources, status)

            elif choice == '3':
                incidents = self.view_incidents()
                for incident in incidents:
                    print(incident)

            elif choice == '4':
                incident_id = input("Enter incident ID to allocate resource to: ")
                resource_id = input("Enter resource ID to allocate: ")
                self.allocate_resource(incident_id, resource_id)

            elif choice == '5':
                incident_id = input("Enter incident ID to reallocate resource from: ")
                resource_id = input("Enter resource ID to reallocate: ")
                self.reallocate_resource(incident_id, resource_id)

            elif choice == '6':
                resources = self.view_resources()
                for resource in resources:
                    print(resource)

            elif choice == '7':
                report = self.get_incident_report()
                for incident in report:
                    print(incident)

            elif choice == '8':
                break
            else:
                print("Invalid choice! Please try again.")

        