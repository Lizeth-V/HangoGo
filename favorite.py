import pymongo
from pymongo import MongoClient
from bson import ObjectId

connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"

def add_to_favorites(user_id, place_id):
    try:
        #connect to cluster and set the server
        client = MongoClient(connection_string)
        db = client[dbname]
        collection = db['User Data']

        #find user and update the favorites by adding to the list
        criteria = {"_id": ObjectId(user_id)}
        data_to_update = {"$addToSet": {"favorite_list": place_id}}

        update_result = collection.update_one(criteria, data_to_update, upsert=True)

        if update_result.upserted_id:
            print("Insertion successful:", update_result.upserted_id)
        else:
            print("Update successful. Matched document:", update_result.matched_count)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        client.close()