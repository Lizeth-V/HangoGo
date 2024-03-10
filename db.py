from pymongo import MongoClient

connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"
# Establish a connection to MongoDB Atlas
client = MongoClient(connection_string)
# Accessing the database
db = client[dbname]
# Accessing the user collection
users_collection = db["User Data"]

# Access the places collection
places_collection = db["Places"]
