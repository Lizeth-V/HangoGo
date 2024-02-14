from pymongo import MongoClient, ASCENDING, errors
import json

connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"
collection_name = "Places"

# Establish a connection to MongoDB Atlas
client = MongoClient(connection_string)

# Accessing the database
db = client[dbname]

# Accessing the collection
collection = db[collection_name]

#If for some reason we have duplicates in our data we want to make sure they only appear once in the database
collection.create_index([("name", ASCENDING), ("address", ASCENDING)], unique=True)

with open('yelp_data3.json', encoding="utf8") as f:
    places = json.load(f)
    for place in places:
        data_to_insert = {
            "name": place['name'],
            "lat": place['latitude'],
            "lon": place['longitude'],
            "address": place['address'],
            "main_type": place['main_type'],
            "sub_types": place['sub_types'],
            "rating": place['stars'],
            "rating_amount": place['review_count'],
            "age": place['age'],
            #"price": place['price_level'],
            #"from": 'google', #might be useful to know where its from, no useability other than knowing.
        }

        try: #running into a error that prevents inserts from proceeding if duplicates so we have to catch the errors.
            result = collection.insert_one(data_to_insert)
            print(f"Insert successful for {place['name']}")
        except errors.DuplicateKeyError:
            print(f"Duplicate key error. Skipping insertion for {place['name']}")
            continue