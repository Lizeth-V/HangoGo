from pymongo import MongoClient, ASCENDING
import time
import datetime
from bson import ObjectId


connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"
collection_name = "ratings"


def accept_recommendation_update(user_id, place_id):
    client = MongoClient(connection_string)
    db = client[dbname]
    
    collection = db[collection_name]

    collection.create_index([("user_id", 1), ("place_id", 1)], unique=True)

    #the index in question
    collection.create_index([("timestamp", ASCENDING)], expireAfterSeconds=2628000)
    
    #for upsert
    criteria = {"user_id": user_id, "place_id": place_id}
    
    #fields to keep
    data_to_insert = {
        "user_id": user_id,
        "place_id": place_id,
        "timestamp": datetime.datetime.utcnow(),
        "feedback": 1
    }

    update_result = collection.update_one(criteria, {"$set": data_to_insert}, upsert=True)

    if update_result.upserted_id:
        print("Insertion successful:", update_result.upserted_id)
    else:
        print("Update successful. Matched document:", update_result.matched_count)

    set_active_place(user_id, place_id)

    client.close()



def add_to_favorites_update(user_id, place_id):
    client = MongoClient(connection_string)
    db = client[dbname]
    
    collection = db[collection_name]

    collection.create_index([("user_id", 1), ("place_id", 1)], unique=True)

    #the index in question
    collection.create_index([("timestamp", ASCENDING)], expireAfterSeconds=2628000)
    
    #for upsert
    criteria = {"user_id": user_id, "place_id": place_id}
    
    #fields to keep
    data_to_insert = {
        "user_id": user_id,
        "place_id": place_id,
        "timestamp": datetime.datetime.utcnow(),
        "feedback": 1
    }

    update_result = collection.update_one(criteria, {"$set": data_to_insert}, upsert=True)

    if update_result.upserted_id:
        print("Insertion successful:", update_result.upserted_id)
    else:
        print("Update successful. Matched document:", update_result.matched_count)

    client.close()


def set_active_place(user_id, place_id):
    try:
        client = MongoClient(connection_string)
        db = client[dbname]
        collection = db['User Data']

        criteria = {"_id": ObjectId(user_id)}
        data_to_insert = {"active_place": place_id}

        print(criteria)

        update_result = collection.update_one(criteria, {"$set": data_to_insert}, upsert=True)

        if update_result.upserted_id:
            print("Insertion successful:", update_result.upserted_id)
        else:
            print("Update successful. Matched document:", update_result.matched_count)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        client.close()

def get_active_place(user_id):
    try:
        client = MongoClient(connection_string)
        db = client[dbname]
        collection = db['User Data']

        criteria = {"_id": ObjectId(user_id)}
        projection = {"active_place": 1, "_id": 0}
        document = collection.find_one(criteria, projection)

        if document:
            return get_place_details(document['active_place'])
        else:
            print("User not found")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        client.close()

def remove_active_place(user_id):
    try:
        client = MongoClient(connection_string)
        db = client[dbname]
        collection = db['User Data']

        criteria = {"_id": ObjectId(user_id)}

        update_result = collection.update_one(criteria, {"$unset": {"active_place": ""}})

        if update_result.modified_count > 0:
            print("Active place removed successfully.")
            return True
        else:
            print("No active place was found or user does not exist.")
            return False

    except Exception as e:
        print("An error occurred:", e)
        return False

    finally:
        # Ensure the MongoDB client is closed
        client.close()

def get_place_details(place_id):
    try:
        client = MongoClient(connection_string)
        db = client[dbname]
        collection = db['Places']

        criteria = {"_id": ObjectId(place_id)}
        projection = {"name": 1, "lat":1, "lon": 1, "address":1, "_id": 1}
        document = collection.find_one(criteria, projection)
        
        if document:
            return document
        else:
            print("User not found")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        client.close()



def decline_recommendation_update(user_id, place_id):
    client = MongoClient(connection_string)
    db = client[dbname]
    
    collection = db[collection_name]

    collection.create_index([("user_id", 1), ("place_id", 1)], unique=True)

    #the index in question
    collection.create_index([("timestamp", ASCENDING)], expireAfterSeconds=2628000)
    
    #for upsert
    criteria = {"user_id": user_id, "place_id": place_id}
    
    #fields to keep
    data_to_insert = {
        "user_id": user_id,
        "place_id": place_id,
        "timestamp": datetime.datetime.utcnow(),
        "feedback": 0
    }

    update_result = collection.update_one(criteria, {"$set": data_to_insert}, upsert=True)

    if update_result.upserted_id:
        print("Insertion successful:", update_result.upserted_id)
    else:
        print("Update successful. Matched document:", update_result.matched_count)

    client.close()


def block_recommendation_update(user_id, place_id):
    client = MongoClient(connection_string)
    db = client[dbname]
    
    collection = db[collection_name]

    collection.create_index([("user_id", 1), ("place_id", 1)], unique=True)
    
    #by not creating an index on the time to live we can just avoid ever regenerating the place

    #for upsert
    criteria = {"user_id": user_id, "place_id": place_id}
    
    #fields to keep
    data_to_insert = {
        "user_id": user_id,
        "place_id": place_id,
        "timestamp": datetime.datetime.utcnow(),
        "feedback": 0
    }

    update_result = collection.update_one(criteria, {"$set": data_to_insert}, upsert=True)

    if update_result.upserted_id:
        print("Insertion successful:", update_result.upserted_id)
    else:
        print("Update successful. Matched document:", update_result.matched_count)

    client.close()

def insert_user_chat(user_id, string, source):
    client = MongoClient(connection_string)
    db = client[dbname]
    
    collection = db['User Chats']

    #fields to keep
    data_to_insert = {
        "user_id": user_id,
        "message": string,
        "source": source,
        "timestamp": datetime.datetime.utcnow(),
       }

    update_result = collection.insert_one(data_to_insert)

    if update_result:
        print("Insertion successful:")
    else:
        print("Update successful. Matched document:", update_result.matched_count)

    client.close()

def delete_user_chat_history(user_id):
    client = MongoClient(connection_string)
    db = client[dbname]
    collection = db['User Chats']

    # Delete all documents where the user_id matches the provided user_id
    delete_result = collection.delete_many({"user_id": user_id})

    if delete_result.deleted_count > 0:
        print(f"Deletion successful. Deleted {delete_result.deleted_count} documents.")
    else:
        print("No documents found for the given user_id.")

    client.close()