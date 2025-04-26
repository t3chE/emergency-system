from typing import Dict, List, Optional
import os
import json
from datetime import datetime
from app.incidents.emerg_incident import Incident, IncidentStatus
from app.resources.emerg_resource import Resource, ResourceStatus
from app.priorities.emerg_priority import Priority
from app.utils.data_persistence import save_data_to_file, load_data_from_file


class EmergencyManagement:
    """Class to manage emergency incidents, resources, and priorities."""

    def __init__(self, data_dir: str = "data"):
        """
        Initializes the EmergencyManagement system.

        Args:
            data_dir (str, optional): The directory to store data files.
                Defaults to "data".
        """
        self.data_dir = data_dir
        self.incidents: Dict[str, Incident] = {}
        self.resources: Dict[str, Resource] = {}
        self.location_mapping: Dict[str, tuple] = self._initialize_location_mapping()  # Use the private method
        self.load_data()  # Load data on startup
        self._add_default_resources()  # Add default resources

    def _add_default_resources(self):
        """Add default resources to the system."""
        if not self.resources:  # Only add default resources if none exist
            default_resources = [
                Resource(name="Fire Truck 1", resource_type="Fire Truck", location="Zone 1", status=ResourceStatus.AVAILABLE),
                Resource(name="Ambulance 1", resource_type="Ambulance", location="Zone 2", status=ResourceStatus.AVAILABLE),
                Resource(name="Police Car 1", resource_type="Police Car", location="Zone 3", status=ResourceStatus.AVAILABLE),
            ]
            for resource in default_resources:
                self.resources[resource.resource_id] = resource    

    def _get_data_file_path(self, filename: str) -> str:
        """
        Constructs the full path to a data file within the data directory.

        Args:
            filename (str): The name of the file.

        Returns:
            str: The full file path.
        """
        return os.path.join(self.data_dir, filename)

    def save_data(self) -> None:
        """Saves incidents and resources to JSON files."""
        print("Saving incidents and resources...")
        try:
            save_data_to_file(
                data={incident_id: incident.to_dict() for incident_id, incident in self.incidents.items()},
                file_path=self._get_data_file_path("incidents.json"),
                data_name="incidents",
            )
            save_data_to_file(
                data={resource_id: resource.to_dict() for resource_id, resource in self.resources.items()},
                file_path=self._get_data_file_path("resources.json"),
                data_name="resources",
            )
            print("Successfully saved incidents and resources.")
        except Exception as e:
            print(f"An error occurred while saving data: {e}")
            # Consider re-raising the exception if you want the caller to handle it
            raise

    def load_data(self) -> None:
        """Loads incidents and resources from JSON files."""
        print("Loading incidents and resources...")
        try:
            incidents_data = load_data_from_file(
                file_path=self._get_data_file_path("incidents.json"), data_name="incidents"
            )
            resources_data = load_data_from_file(
                file_path=self._get_data_file_path("resources.json"), data_name="resources"
            )
            self.incidents = {incident_id: Incident.from_dict(data) for incident_id, data in incidents_data.items()}
            self.resources = {resource_id: Resource.from_dict(data) for resource_id, data in resources_data.items()}
            print("Successfully loaded incidents and resources.")
        except Exception as e:
            print(f"An error occurred while loading data: {e}")
            #  Do NOT re-raise here, because an empty system state is valid on first run
            #   Instead, ensure that the program can start with empty data.
            self.incidents = {}
            self.resources = {}

    def _initialize_location_mapping(self) -> Dict[str, tuple]:
        """Initializes the location mapping for resources (private method)."""
        return {
            "Zone 1": (51.4592, -0.2567),  # Example coordinates
            "Zone 2": (51.4761, -0.1441),
            "Zone 3": (51.4575, -0.1165),
        }

    def process_resource_allocation(self) -> None:
        """Allocate available resources to open incidents based on priority."""
        available_resources = [res for res in self.resources.values() if res.status == ResourceStatus.AVAILABLE]
        open_incidents = sorted(
            [inc for inc in self.incidents.values() if inc.status in (IncidentStatus.OPEN, IncidentStatus.IN_PROGRESS)],
            key=lambda inc: inc.priority,  # Sort by priority
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
                    (
                        res
                        for res in available_resources
                        if res.resource_type == required_resource_type and res.status == ResourceStatus.AVAILABLE
                    ),
                    None,
                )
                if suitable_resource:
                    self.allocate_resource(incident.incident_id, suitable_resource.resource_id)
                    available_resources.remove(
                        suitable_resource
                    )  # Ensure resource isn't allocated again in this cycle

        print("\n--- Resource Allocation Processed ---")
        for incident_id, incident in self.incidents.items():
            print(f"Incident {incident_id}: Assigned Resources: {incident.assigned_resources}")
        for resource_id, resource in self.resources.items():
            print(
                f"Resource {resource_id}: Status: {resource.status.value}, Assigned to: {resource.assigned_incident_id}"
            )
        print("-------------------------------------\n")

    def add_incident(
        self, location: str, emergency_type: str, priority: Priority, required_resources: List[str]
    ) -> str:
        """Add a new incident to the system."""
        incident = Incident(location, emergency_type, priority, required_resources)
        self.incidents[incident.incident_id] = incident  # Store the incident
        self.process_resource_allocation()  # Allocate resources immediately
        return incident.incident_id

    def update_incident(
        self,
        incident_id: str,
        location: Optional[str] = None,
        emergency_type: Optional[str] = None,
        priority: Optional[Priority] = None,  # Use Priority Enum
        required_resources: Optional[List[str]] = None,
        status: Optional[IncidentStatus] = None,  # Use IncidentStatus Enum
    ) -> bool:
        """Update an existing incident."""
        incident = self.incidents.get(incident_id)  # Directly get the incident by its ID
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
                incident.update_status(status)  # Use the update_status method
            self.process_resource_allocation()
            return True
        return False

    def view_incidents(self) -> List[Incident]:
        """View all incidents."""
        return list(self.incidents.values())  # Return a list of Incident objects

    def view_resources(self) -> List[Resource]:
        """View all resources."""
        return list(self.resources.values())

    def allocate_resource(self, incident_id: str, resource_id: str) -> bool:
        """Allocates a specific resource to a specific incident."""
        resource = self.resources.get(resource_id)
        incident = self.incidents.get(incident_id)
        if resource and resource.status == ResourceStatus.AVAILABLE and incident:
            resource.status = ResourceStatus.ASSIGNED
            resource.assigned_incident_id = incident_id
            incident.assigned_resources.append(resource_id)
            return True
        return False

    def reallocate_resource(self, new_incident_id: str, resource_id: str) -> bool:
        """Reallocates a resource from its current incident to a new incident."""
        resource = self.resources.get(resource_id)
        new_incident = self.incidents.get(new_incident_id)

        if resource and new_incident:
            current_incident_id = resource.assigned_incident_id
            if current_incident_id:
                current_incident = self.incidents.get(current_incident_id)
                if current_incident:
                    current_incident.assigned_resources.remove(resource_id)
            resource.assigned_incident_id = new_incident_id
            resource.status = ResourceStatus.ASSIGNED
            new_incident.assigned_resources.append(resource_id)
            return True
        return False

    def reallocate_resources_for_new_high_priority(self, new_incident_id: str) -> None:
        """
        Trigger resource reallocation when a new high-priority incident is added.
        """
        incident = self.incidents.get(new_incident_id)
        if incident and incident.priority == Priority.HIGH:  # Adjust based on your highest priority
            print(f"Initiating resource reallocation for new high-priority incident: {new_incident_id}")
            self.process_resource_allocation()

    def get_incident_report(self) -> List[Incident]:
        """Generate a report of all incidents."""
        return list(self.incidents.values())

    def get_active_incidents(self) -> List[Incident]:
        """Get all active incidents."""
        return [incident for incident in self.incidents.values() if incident.status == IncidentStatus.OPEN]

    def run(self) -> None:
        """Run the emergency management system."""
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
            try:
                if choice == "1":
                    location = input("Enter location (e.g., Zone 1, Zone 2...): ")
                    emergency_type = input("Enter emergency type (natural disaster, medical, or human-caused): ")
                    priority_str = input("Enter priority (HIGH, MEDIUM, LOW): ")
                    try:
                        priority = Priority[priority_str.upper()]
                    except KeyError:
                        print(
                            f"Invalid priority: {priority_str}. Must be one of {list(Priority.__members__.keys())}."
                        )
                        continue  # Go back to the main menu
                    required_resources = input(
                        "Enter required resources (comma separated, e.g., Fire Truck, Ambulance): "
                    ).split(",")
                    new_incident_id = self.add_incident(location, emergency_type, priority, required_resources)
                    print(f"Incident added with ID: {new_incident_id}")
                    incident = self.incidents.get(new_incident_id)  # added get
                    if incident and incident.priority == Priority.HIGH:
                        self.reallocate_resources_for_new_high_priority(new_incident_id)

                elif choice == "2":
                    incident_id = input("Enter incident ID to update: ")
                    location = input("Enter new location (or leave blank): ") or None
                    emergency_type = input("Enter new emergency type (or leave blank): ") or None
                    priority_str = input("Enter new priority (HIGH, MEDIUM, LOW, or leave blank): ") or None
                    priority = Priority[priority_str.upper()] if priority_str else None # convert to enum
                    required_resources = (
                        input("Enter new required resources (comma separated, or leave blank): ").split(",") or None
                    )
                    status_str = input("Enter new status (OPEN, IN_PROGRESS, RESOLVED, CLOSED, or leave blank): ") or None
                    status = IncidentStatus[status_str.upper()] if status_str else None # convert to enum

                    if self.update_incident(
                        incident_id, location, emergency_type, priority, required_resources, status
                    ):
                        print(f"Incident {incident_id} updated successfully.")
                    else:
                        print(f"Incident with ID {incident_id} not found.")

                elif choice == "3":
                    incidents = self.view_incidents()
                    if incidents:
                        for incident in incidents:
                            print(incident)
                    else:
                        print("No incidents to display.")

                elif choice == "4":
                    incident_id = input("Enter incident ID to allocate resource to: ")
                    resource_id = input("Enter resource ID to allocate: ")
                    if self.allocate_resource(incident_id, resource_id):
                        print(f"Resource {resource_id} allocated to incident {incident_id}.")
                    else:
                        print(f"Failed to allocate resource.  Check IDs and resource availability.")

                elif choice == "5":
                    incident_id = input("Enter new incident ID to reallocate resource to: ")
                    resource_id = input("Enter resource ID to reallocate: ")
                    if self.reallocate_resource(incident_id, resource_id):
                        print(f"Resource {resource_id} reallocated to incident {incident_id}.")
                    else:
                        print("Failed to reallocate resource. Check IDs and resource assignment.")

                elif choice == "6":
                    resources = self.view_resources()
                    if resources:
                        for resource in resources:
                            print(f"Resource ID: {resource.resource_id}")
                            print(f"Name: {resource.name}")
                            print(f"Type: {resource.resource_type}")
                            print(f"Location: {resource.location}")
                            print(f"Status: {resource.status.value}")
                            print(f"Assigned Incident ID: {resource.assigned_incident_id or 'None'}\n")
                    else:
                        print("No resources to display.")

                elif choice == "7":
                    report = self.get_incident_report()
                    if report:
                        for incident in report:
                            print(incident)
                    else:
                        print("No incidents to report.")

                elif choice == "8":
                    # Save data before exiting
                    self.save_data()
                    print("Exiting Emergency Management System.  Goodbye!")
                    break
                else:
                    print("Invalid choice! Please try again.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                # Consider logging the error for debugging
                print("Please try again.")  # Provide a user-friendly message

if __name__ == "__main__":
    ems = EmergencyManagement()
    ems.run()

        