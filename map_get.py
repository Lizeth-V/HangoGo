from db import users_collection, places_collection
# functions that will fetch the location information for Map Page (Lizeth)
# 2 seperate functions for yelp locations and google places

def getP_google():
    pass

def getP_yelp():
    pass

def get_place_info(place_name):
    place = places_collection.find_one({'name': place_name})
    if place:
        weblink = place.get('weblink')
        longitude = place.get('lon')
        latitude = place.get('lat')
        return {'weblink': weblink, 'longitude': longitude, 'latitude': latitude}
    else:
        return None