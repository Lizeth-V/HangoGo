from pymongo import MongoClient
from bson import ObjectId

# MongoDB connection details
connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"
collection_name = "Places"

# Connect to MongoDB
client = MongoClient(connection_string)
db = client[dbname]
collection = db[collection_name]

# Function to update documents
def update_documents():
    # Iterate through documents in the collection
    for document in collection.find():
        # Extract lat and lon values
        lat = document.get("lat")
        lon = document.get("lon")

        # Create a new location field with 2dsphere index structure
        location_field = {
            "type": "Point",
            "coordinates": [lon, lat]
        }

        # Update the document with the new location field
        collection.update_one(
            {"_id": document["_id"]},
            {"$set": {"location": location_field}}
        )

# Create a 2dsphere index on the location field
collection.create_index([("location", "2dsphere")])

# Update documents
update_documents()

# Close the MongoDB connection
client.close()

print("Documents updated successfully.")
