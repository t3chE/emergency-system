from app.incidents import incident
from app.management import management
from app.priorities import priority
from app.resources import resource

if __name__ == "__main__":
    ems = management() # Import the management module from the app package
    ems.run() 