from pymongo import MongoClient, ASCENDING, DESCENDING
from bson import ObjectId


connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"


#returns the list of user history entries form mongo using our mongo program file
def get_user_history(user_id):
    collection_name = "User Chats"

    client = MongoClient(connection_string)
    db = client[dbname]
    collection = db[collection_name]

    ##connect to mongo collection

    #get the user's history
    query = {
        'user_id': user_id,
        }
    
    #keep the source and message for deciding how to display the history later
    projection = {'message': 1, 'source':1, '_id': 0}

    #get user feedback in order of date oldest -> newest
    chat_history = list(collection.find(query, projection).sort("timestamp", ASCENDING))

    return chat_history

#deprecated, though may be useful in the future
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
