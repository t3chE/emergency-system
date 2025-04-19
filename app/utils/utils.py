import math
def calculate_distance(coord1, coord2):
    """
    Calculate the Haversine distance between two points on the Earth specified by latitude and longitude.
    
    Parameters:
    coord1 (tuple): A tuple containing the latitude and longitude of the first point.
    coord2 (tuple): A tuple containing the latitude and longitude of the second point.
    
    Returns:
    float: The distance between the two points in kilometers.
    """
    R = 6371.0  # Radius of the Earth in kilometers

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance