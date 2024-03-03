from pymongo import MongoClient, ASCENDING
import time
import datetime


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
        "feedback": 1 #what about add one each time?
    }

    update_result = collection.update_one(criteria, {"$set": data_to_insert}, upsert=True)

    if update_result.upserted_id:
        print("Insertion successful:", update_result.upserted_id)
    else:
        print("Update successful. Matched document:", update_result.matched_count)

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
        "feedback": 0 #what about subtract by 1 each time?
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