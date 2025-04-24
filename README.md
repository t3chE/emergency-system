# EmergencySystem

## Overview
The EmergencySystem is a Python-based application designed to manage emergency incidents and resources efficiently. It allows users to add, update, and view incidents, allocate and reallocate resources, and generate reports. The system prioritizes incidents based on their urgency and ensures optimal resource allocation.

## Features

### Incident Management:
- Add, update, and view incidents.
- Prioritize incidents based on urgency (`HIGH`, `MEDIUM`, `LOW`).
- Track the status of incidents (`OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`).

### Resource Management:
- Add and view resources.
- Allocate resources to incidents based on priority and type.
- Reallocate resources between incidents.

### Reports:
- Generate detailed reports of all incidents and their assigned resources.

### Data Persistence:
- Save and load incidents and resources to/from JSON files for persistence across sessions.

## Technologies Used
- **Python**: Core programming language.
- **Object-Oriented Programming (OOP)**: Used for modular and maintainable code.
- **JSON**: For data persistence.
- **Enums**: For managing incident priorities and statuses.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher installed on your system.

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/EmergencySystem.git
    cd EmergencySystem
    ```
    
2. Install dependencies (if any):
    ```bash
    pip install -r requirements.txt
    ```
3. Run the program:
    ```bash
    python main.py
    ```

## Usage

### Main Menu
When you run the program, you will see the following menu:

==========================================
Welcome to the Emergency Management System
==========================================

1. Add Incident
2. Update Incident
3. View Incidents
4. Allocate Resource
5. Reallocate Resource
6. View Resources
7. Generate Incident Report
8. Exit

==========================================

#### Options
1. **Add Incident**:
    - Enter details such as location, emergency type, priority, and required resources.
    - The system will automatically allocate resources based on availability and priority.
2. **Update Incident**:
    - Update details of an existing incident, such as location, priority, or status.
3. **View Incidents**:
    - View all incidents in the system, including their details and assigned resources.
4. **Allocate Resource**:
    - Manually allocate a resource to an incident.
5. **Reallocate Resource**:
    - Reassign a resource from one incident to another.
6. **View Resources**:
    - View all resources in the system, including their status and assigned incident (if any).
7. **Generate Incident Report**:
    - Generate a detailed report of all incidents.
8. **Exit**:
    - Save data and exit the program.

### Example Workflow
1. **Add a new incident**:
    ```bash
    Enter location: Downtown
    Enter emergency type: Fire
    Enter priority: HIGH
    Enter required resources: Firetruck
    ```
    **Output**:
    ```
    Incident added successfully. Resources allocated: Firetruck.
    ```

2. **View resources**:
    ```bash
    Resource: Firetruck | Status: Assigned | Incident: Downtown Fire
    ```

3. **Reallocate a resource**:
    ```bash
    Resource: Firetruck reassigned to Uptown Flood.
    ```

## Testing
The program includes unit tests to ensure functionality. To run the tests:
```bash
python -m unittest discover tests
```

## Future Improvements
- **Real-Time Maps**: Integrate mapping APIs to visualize incidents and resources.
- **GUI**: Add a graphical user interface for better usability.
- **Advanced Algorithms**: Implement optimization algorithms for resource allocation.
- **Database Integration**: Replace JSON storage with a relational or NoSQL database for scalability.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add feature-name"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-name
    ```
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or feedback, please contact:
- **Name**: Gus  
- **Email**: your.email@example.com  
- **GitHub**: [t3chE](https://github.com/your-t3chE)  