from pymongo import MongoClient
from bson import ObjectId

#run once per db update
#adds the location field to the place database for geo-loaction queries

#mongo
connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"
collection_name = "Places"

client = MongoClient(connection_string)
db = client[dbname]
collection = db[collection_name]

#update the collection with a lcoation field so i can do radius in the return
def update_documents():
    for document in collection.find():
        lat = document.get("lat")
        lon = document.get("lon")

        #new field
        location_field = {
            "type": "Point",
            "coordinates": [lon, lat]
        }

        #update every doc
        collection.update_one(
            {"_id": document["_id"]},
            {"$set": {"location": location_field}}
        )

collection.create_index([("location", "2dsphere")])

update_documents()

client.close()

print("Documents updated successfully.")
