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
        self.incidents: Dict[str, Incident] = {}
        self.resources: Dict[str, Resource] = {}
        self.location_mapping = {}
        self.initialize_location_mapping()

    def save_data(self, incidents_file, resources_file):
        """ Save incidents and resources to JSON files """
        print("Saving incidents and resources...")
        print("Resources before saving:")
        for resource_id, resource in self.resources.items():
            print(f"Resource {resource_id}: {resource.to_dict()}")  # Debugging statement
        save_incidents_to_file(self.incidents, incidents_file)   
        save_resources_to_file(self.resources, resources_file)

    def load_data(self, incidents_file, resources_file):
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

    def process_resource_allocation(self):
        """ Allocate available resources to open incidents based on priority. """
        available_resources = [res for res in self.resources.values() if res.status == ResourceStatus.AVAILABLE]
        open_incidents = sorted(
            [inc for inc in self.incidents.values() if inc.status == IncidentStatus.OPEN or inc.status == IncidentStatus.IN_PROGRESS],
            key=lambda inc: inc.priority,  # Sort by priority (you might need to adjust the sorting order)
            reverse=True,  # Assuming higher priority enums come first
        )

        # Reset assignments before re-allocating
        for resource in self.resources.values():
            if resource.status == ResourceStatus.ASSIGNED:
                resource.status = ResourceStatus.AVAILABLE
                resource.assigned_incident_id = None
        for incident in self.incidents.values():
            incident.assigned_resources = []

        for incident in open_incidents:
            for required_resource_type in incident.required_resources:
                # Find an available resource of the required type
                suitable_resource = next(
                    (res for res in available_resources if res.resource_type == required_resource_type and res.status == ResourceStatus.AVAILABLE),
                    None,
                )
                if suitable_resource:
                    self.allocate_resource(incident.incident_id, suitable_resource.resource_id)
                    available_resources.remove(suitable_resource) # Ensure resource isn't allocated again in this cycle

        print("\n--- Resource Allocation Processed ---")
        for incident_id, incident in self.incidents.items():
            print(f"Incident {incident_id}: Assigned Resources: {incident.assigned_resources}")
        for resource_id, resource in self.resources.items():
            print(f"Resource {resource_id}: Status: {resource.status.value}, Assigned to: {resource.assigned_incident_id}")
        print("-------------------------------------\n")    

    def add_incident(self, location, emergency_type, priority, required_resources):
        """ Add a new incident to the system """

        incident = Incident(location, emergency_type, priority, required_resources)
        self.incidents[incident.incident_id] = incident # Store the incident in the dictionary

        for resource_id in required_resources:
            resource = self.resources.get(resource_id)
            if resource and resource.status == ResourceStatus.AVAILABLE:  # Only assign if available
                resource.status = ResourceStatus.ASSIGNED
                incident.assigned_resources.append(resource_id)
                resource.assigned_incident_id = incident.incident_id

        self.process_resource_allocation() # Reallocate resources after adding a new incident
        
        return incident.incident_id

    def update_incident(self, incident_id: str, location: str = None, emergency_type: str = None,
            priority: str = None, required_resources: List[str] = None, status: str = None):    
        """ Update an existing incident """

        incident = self.incidents.get(incident_id) # Directly get the incident by its ID
        if incident:
            if location:
                incident.location = location
            if emergency_type:
                incident.emerg_type = emergency_type
            if priority:
                try:
                    incident.priority = Priority[priority.upper()]
                except KeyError:
                    print(f"Invalid priority level: {priority}. Must be one of {list(Priority.__members__.keys())}.")
                    return False
                
            self.process_resource_allocation()    
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
    
    def allocate_resource(self, incident_id, resource_id):
        resource = self.resources.get(resource_id)
        if resource and resource.status == ResourceStatus.AVAILABLE:
            resource.status = ResourceStatus.ASSIGNED
            resource.assigned_incident_id = incident_id
            incident = self.incidents.get(incident_id)
            if incident:
                incident.assigned_resources.append(resource_id)
                return True
        return False

    def reallocate_resource(self, incident_id, resource_id):
        resource = self.resources.get(resource_id)
        if resource:
        # Remove resource from the current incident
            current_incident = self.incidents.get(resource.assigned_incident_id)
            if current_incident:
                current_incident.assigned_resources.remove(resource_id)

            # Assign resource to the new incident
            resource.assigned_incident_id = incident_id
            resource.status = ResourceStatus.ASSIGNED
            new_incident = self.incidents.get(incident_id)
            if new_incident:
                new_incident.assigned_resources.append(resource_id)
                return True
        return False
    
    def reallocate_resource_for_new_high_priority(self, new_incident_id: str):
        """ Trigger resource reallocation when a new high-priority incident is added. """
        incident = self.incidents.get(new_incident_id)
        if incident and incident.priority == Priority.HIGH: # Adjust based on your highest priority
            print(f"Initiating resource reallocation for new high-priority incident: {new_incident_id}")
            self.process_resource_allocation()

    def get_incident_report(self) -> List[Incident]:
        """ Generate a report of all incidents """
        return self.incidents
    
    def get_active_incidents(self) -> List[Incident]:
        """ Get all active incidents """
        return [incident for incident in self.incidents if incident.status == IncidentStatus.OPEN]
    
    def run(self):
        """ Run the emergency management system """
        # Load initial data
        self.load_data('incidents.json', 'resources.json')

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

            choice = input("Please enter an option: ")
            if choice == '1':
                location = input("Enter location (e.g., Zone 1, Zone 2...): ")
                emergency_type = input("Enter emergency type (natural disaster, medical or human-caused): ")
                priority = input("Enter priority (CAT_1 - CAT_4): ")
                required_resources = input("Enter required resources (comma separated, e.g., Fire Truch, Ambulance): ").split(',')
                self.add_incident(location, emergency_type, priority, required_resources)
                new_incident_id = self.add_incident(location, emergency_type, priority, required_resources)
                incident = self.incidents.get(new_incident_id)
                if incident and incident.priority == Priority.CATEGORY_1:
                    self.reallocate_resources_for_new_high_priority(new_incident_id)

            elif choice == '2':
                incident_id = input("Enter incident ID to update: ")
                location = input("Enter new location (or leave blank): ")
                emergency_type = input("Enter new emergency type (or leave blank): ")
                priority = input("Enter new priority (CAT_1 to CAT_4, or leave blank): ")
                required_resources = input("Enter new required resources (comma separated, or leave blank): ").split(',')
                status = input("Enter new status (NEW, OPEN, ASSIGNED, IN_PROGRESS, RESOLVED, or leave blank): ")
                self.update_incident(incident_id, location, emergency_type, priority, required_resources, status)
                if self.update_incident(incident_id, location, emergency_type, priority, required_resources, status):
                    incident = self.incidents.get(incident_id)
                    if priority:
                        self.reallocate_resources_for_priority_change(incident_id)
                    if status:
                        self._allocate_resources()
                else:
                    print(f"Incident with ID {incident_id} not found.")
                    
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
                # Save data before exiting
                self.save_data('incidents.json', 'resources.json')
                break
            else:
                print("Invalid choice! Please try again.")

        