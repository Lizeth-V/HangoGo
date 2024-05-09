# Nhu
# recommend place after combing all user_ids and location

from pymongo import MongoClient
import generate_model as m
import return_highest_rec as rec_list
import pandas as pd
import return_highest_rec as retH

# sample user_ids and location for testing
user_ids = ['6568cbef4a9658311b3ee704', '6615b194f92286e38d5f91b2']
location = [[33.8347516,-117.911732]]
usernames = ['aidan', 'gloria']

# username to userid
def username_to_userid(usernames):
    connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
    client = MongoClient(connection_string)
    db = client["Hango"]
    collection = db['User Data']
    id_list = []
    for username in usernames:
        try:
            user_object = collection.find({"username": username})[0]
            id_list.append(str(user_object['_id']))
        except Exception as e:
            print(f"{username} does not exist.")
            return e
    return id_list   


#find center location if multiple locations, if not just return location
def location_helper(location):
    if len(location) == 1:
        return location[0]
    else:
        lat = [p[0] for p in location]
        long = [p[1] for p in location]
        centroid = [sum(lat) / len(location), sum(long) / len(location)]
        return centroid

