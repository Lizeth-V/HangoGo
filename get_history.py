from pymongo import MongoClient, ASCENDING
from bson import ObjectId


connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"


def get_user_history(user_id):
    collection_name = "ratings"

    client = MongoClient(connection_string)
    db = client[dbname]
    collection = db[collection_name]

    query = {
        'user_id': user_id,
        }
    
    projection = {'place_id': 1, 'feedback': 1, '_id': 0}

    #get user feedback in order of date oldest -> newest
    chat_history = list(collection.find(query, projection).sort("timestamp", ASCENDING))

    return chat_history

def change_id_to_name(history_list):
    client = MongoClient(connection_string)
    db = client[dbname]

    collection_name = "Places"

    collection = db[collection_name]

    #get every place and save the name and feedback, thats all we need to print out the history
    #maybe weblink might help

    for history in history_list:
        place_id = history['place_id']

        query = {
        '_id': ObjectId(place_id),
        }

        projection = {'name': 1, '_id': 0}

        get_name = list(collection.find(query, projection))[0]
        
        history['name'] = get_name['name']

        #remove the id, its not needed
        del history['place_id']

    return history_list


def pull_history(user_id):
    return change_id_to_name(get_user_history(user_id))
#Top level function
