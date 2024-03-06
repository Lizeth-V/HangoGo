from pymongo import MongoClient
from bson import ObjectId
import random
import geocoder

connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"


def mi_2_meters(miles):
    return miles*1609

def get_highest_list(u_id):    
    client = MongoClient(connection_string)
    db = client[dbname]

    collection_name = "User Data"

    collection = db[collection_name]

    query = {"_id": ObjectId(u_id)}

    user_object = collection.find_one(query)

    if user_object:
        top_choices = user_object['rec_probs']
        return top_choices
    else:
        print("Could Not Find User")
        return None
    
    client.close()

def match_highest_list(top_choices, radius = 500, place_type = None):
    print(top_choices)

    client = MongoClient(connection_string)
    db = client[dbname]

    collection_name = "Places"

    collection = db[collection_name]

    user_loc = geocoder.ip('me').latlng

    center_point = {
        "lat": user_loc[0],
        "lon": user_loc[1]
    }

    radius = mi_2_meters(radius)

    # Convert radius to radians
    radius_radians = radius / 6371  # Earth's radius is approximately 6371 km

    object_ids = [ObjectId(choice) for choice in top_choices[:10]]

    query = {
        '_id': {'$in': object_ids},
    }

    if place_type:
        query['place_type'] = place_type

    #return top 5 and choose randomly giving higher weight to better recommendations.
    result = list(collection.find(query).limit(5))

    best = random.choice(result)

    print(best)

#temp = get_highest_list('6568cbef4a9658311b3ee704')
#match_highest_list(top_choices=temp)

