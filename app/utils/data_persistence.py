import json
from app.incidents.emerg_incident import Incident
from app.resources.emerg_resource import Resource


def save_incidents_to_file(incidents, file_path):
    """ Save incidents to a JSON file """
    print(f"Saving incidents to {file_path}:")
    with open(file_path, 'w') as f:
        json.dump({incident_id: incident.to_dict() for incident_id, incident in incidents.items()}, f, indent=4)


def load_incidents_from_file(file_path):
    """ Load incidents from a JSON file """
    try:
        with open(file_path, 'r') as f:
            incidents_data = json.load(f)
            print(f"Loaded incidents from {file_path}: {incidents_data}")  # Correct debugging statement
            return {incident_id: Incident.from_dict(data) for incident_id, data in incidents_data.items()} 
    except FileNotFoundError:
        print(f"File {file_path} not found. Starting with an empty incidents dictionary.")
        return {}


def save_resources_to_file(resources, file_path):
    """ Save resources to a JSON file """ 
    print(f"Saving resources to {file_path}:")
    for key, resource in resources.items():
        print(f"Resource {key}: {resource.to_dict()}")  # Debugging statement
    with open(file_path, 'w') as f:
        json.dump({key: resource.to_dict() for key, resource in resources.items()}, f, indent=4)


def load_resources_from_file(file_path):
    """ Load resources from a JSON file """
    try:
        with open(file_path, 'r') as f:
            resources_data = json.load(f)
            return {key: Resource.from_dict(data) for key, data in resources_data.items()}
    except FileNotFoundError:
        print(f"File {file_path} not found. Starting with an empty resources dictionary.")
        return {} 