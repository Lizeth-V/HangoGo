#user_ids in an array
#location_pref (one of locations, center of location, or new location)

from pymongo import MongoClient

connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
client = MongoClient(connection_string)
db = client["Hango"]

user_ids = ['6568cbef4a9658311b3ee704', '6615b194f92286e38d5f91b2']

def combine_ratings(user_ids):
    user_ratings = db['ratings']
    json_list = []
    for user_id in user_ids:
        json_list.append({"user_id": user_id})

    combined_query = {
    "$or": json_list
    }

    result = user_ratings.find(combined_query)
    # Print the matching documents
    for doc in result:
        print(doc)

def get_multi_rec(user_ids, location_pref):

    combine_ratings(user_ids)

    #combine all users' ratings to find recommendation

    #do that based on location choice
    #if location_pref is only one location, then just take that location
    #if location_pref is multiple locations, find the center