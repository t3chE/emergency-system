import json
import os
from typing import Dict, Any
from app.incidents.emerg_incident import Incident
from app.resources.emerg_resource import Resource


def save_data_to_file(data: Dict[str, Any], file_path: str, data_name: str = "data") -> None:
    """
    Saves a dictionary to a JSON file.

    Args:
        data (dict): The data to save.
        file_path (str): The path to the file.
        data_name (str, optional): A descriptive name for the data (for logging).
            Defaults to "data".
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure directory exists
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Successfully saved {data_name} to {file_path}")
    except (IOError, OSError) as e:
        print(f"Error saving {data_name} to {file_path}: {e}")
        raise  # Re-raise to allow caller to handle or log

def load_data_from_file(file_path: str, data_name: str = "data") -> Dict[str, Any]:
    """
    Loads a dictionary from a JSON file.  Handles file not found and other errors.

    Args:
        file_path (str): The path to the file.
        data_name (str, optional): A descriptive name for the data (for logging).
            Defaults to "data".

    Returns:
        dict: The loaded dictionary.  Returns an empty dictionary if the file
              does not exist or is empty.

    Raises:
        IOError: If there is an error reading the file.
        OSError: A general operating system error occurred.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        print(f"Successfully loaded {data_name} from {file_path}")
        return data
    except FileNotFoundError:
        print(f"File {file_path} not found.  Returning empty {data_name} dictionary.")
        return {}  # Consistent return of an empty dict on file not found
    except (IOError, OSError, json.JSONDecodeError) as e:
        print(f"Error loading {data_name} from {file_path}: {e}")
        raise  # Re-raise the exception


def save_incidents_to_file(incidents: Dict[str, Incident], file_path: str) -> None:
    """Saves incidents to a JSON file."""
    incident_data = {incident_id: incident.to_dict() for incident_id, incident in incidents.items()}
    save_data_to_file(incident_data, file_path, "incidents")


def load_incidents_from_file(file_path: str) -> Dict[str, Incident]:
    """Loads incidents from a JSON file."""
    incident_data = load_data_from_file(file_path, "incidents")
    return {incident_id: Incident.from_dict(data) for incident_id, data in incident_data.items()}


def save_resources_to_file(resources: Dict[str, Resource], file_path: str) -> None:
    """Saves resources to a JSON file."""
    resource_data = {key: resource.to_dict() for key, resource in resources.items()}
    save_data_to_file(resource_data, file_path, "resources")


def load_resources_from_file(file_path: str) -> Dict[str, Resource]:
    """Loads resources from a JSON file."""
    resource_data = load_data_from_file(file_path, "resources")
    return {key: Resource.from_dict(data) for key, data in resource_data.items()} 