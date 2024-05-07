# Geting the top locations with the highest rating in a 15 mile radius from the users location
from db import places_collection


def getTop_locations(lat, long, radius):
    # Convert radius from miles to meters
    radius_meters = radius * 1609.34

    center_point = {
        "type": "Point",
        "coordinates": [long, lat]
    }

    query = {
        'location': {
            '$geoWithin': {
                '$centerSphere': [
                    center_point['coordinates'],
                    radius_meters / 6371000  # Convert radius to radians
                ]
            }
        }
    }

    try:
        # Query the database and sort by rating
        result = places_collection.find(query).sort('rating', -1).limit(10)
        # Convert the MongoDB cursor to a list of dictionaries for easier handling
        # top_locations = list(result)
        return result
    except Exception as e:
        # Handle any exceptions, such as database errors
        print("An error occurred:", e)
        return []
