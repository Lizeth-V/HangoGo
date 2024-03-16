from pymongo import MongoClient
from bson import ObjectId
import random
import geocoder
from geopy.geocoders import Nominatim

connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"


def mi_2_meters(miles):
    return miles*1609

#Nhu's code
def get_location(u_id):
    app = Nominatim(user_agent="test")
    # UNCOMMENT CODE ONCE USERS HAVE THE CORRECT ADDRESSES (NOT DUMMY ADDRESSES)
    # query = { "_id": ObjectId(u_id) }
    # user_col = collection.find_one(query)['address'] #return {'street': '', 'city': '', 'state': 'CA', 'zip_code': '', 'country': 'USA'}
    # user_add = user_col['street'] + ', ' + user_col['city'] + ', ' + user_col['state'] 
    user_add = str(input('Enter city: '))
    address = app.geocode(user_add).raw
    # Get long and lat from data
    user_loc = [float(address['lat']), float(address['lon'])]
    return user_loc

def get_highest_list(u_id):    
    #get the list of places in probability order and return
    client = MongoClient(connection_string)
    db = client[dbname]

    collection_name = "User Data"

    collection = db[collection_name]

    query = {"_id": ObjectId(u_id)}
    #search for the user in the collection and save the list   

    user_object = collection.find_one(query)

    if user_object:
        top_choices = user_object['rec_probs']
        return top_choices
    else:
        print("Could Not Find User")
        return None
    
    client.close()

def match_highest_list(top_choices, radius = 500, place_type = None):
    #match the place ids in the top_choices list and return one or change it to many.
    client = MongoClient(connection_string)
    db = client[dbname]

    collection_name = "Places"

    collection = db[collection_name]

    #replace this with the html gps location coordinates, more accurate.

    user_loc = geocoder.ip('me').latlng #get_location(u_id) later when using locations from database, change get_location code too!


    center_point = {
        "lat": user_loc[0],
        "lon": user_loc[1]
    }

    radius = mi_2_meters(radius)

    #conversion for radius calculation
    radius_radians = radius / 6371  # Earth's radius is approximately 6371 km

    object_ids = [ObjectId(choice) for choice in top_choices[:10]]

    #query the objects in the list
    query = {
        '_id': {'$in': object_ids},
    }

    #if the type is included in the function call add it to the query
    if place_type:
        query['place_type'] = place_type

    #return top 5 and choose randomly giving higher weight to better recommendations.
    result = list(collection.find(query).limit(5))

    best = random.choice(result)

    return best
    #print(best)

#temp = get_highest_list('6568cbef4a9658311b3ee704')
#match_highest_list(top_choices=temp)

