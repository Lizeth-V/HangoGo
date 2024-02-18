import time
from pymongo import MongoClient

connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"
collection_name = "ratings"

def main():
    #TESTING ARTIFICIAL INSERT
    accept_recommendation_update('6567dcefba91df16f20f718d', '65c7c805d20df83fcf08aa71')

def accept_recommendation_update(user_id, place_id):
    client = MongoClient(connection_string)
    db = client[dbname]
    #use mongo  to connect to hango db

    #access specifically rating db collection
    collection = db[collection_name]

    #package unit
    data_to_insert = {
    "user_id":user_id,
    "place_id":place_id,
    "timestamp": time.time(),
    "feedback": 1
    }

    #make sure it inserts
    try:
        insert_result = collection.insert_one(data_to_insert)
        print("Insertion successful:", insert_result.inserted_id)
    except Exception as e:
        print("Error occurred:", e)

    client.close()

def add_to_favorites_update(user_id, place_id):

    client = MongoClient(connection_string)
    db = client[dbname]

    #use mongo  to connect to hango db

    #access specifically rating db collection
    collection = db[collection_name]

    #package unit
    data_to_insert = {
    "user_id":user_id,
    "place_id":place_id,
    "timestamp": time.time(),
    "feedback": 1
    }

    insert_result = collection.insert_one(data_to_insert)


def decline_recommendation_update(user_id, place_id):
    client = MongoClient(connection_string)
    db = client[dbname]
    #use mongo  to connect to hango db

    #access specifically rating db collection
    collection = db[collection_name]

     #package unit
    data_to_insert = {
    "user_id":user_id,
    "place_id":place_id,
    "timestamp": time.time(),
    "feedback": 0
    }

    insert_result = collection.insert_one(data_to_insert)

def block_recommendation_update(user_id, place_id):
    client = MongoClient(connection_string)
    db = client[dbname]
    #use mongo  to connect to hango db

    #access specifically rating db collection
    collection = db[collection_name]

     #package unit
    data_to_insert = {
    "user_id":user_id,
    "place_id":place_id,
    "timestamp": time.time(),
    "feedback": 0
    }

    insert_result = collection.insert_one(data_to_insert)

main()

