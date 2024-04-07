from geopy.geocoders import Nominatim
from pymongo import MongoClient
from bson import ObjectId

connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
client = MongoClient(connection_string)
db = client["Hango"]
collection_name = "User Data"
collection = db[collection_name]

def add_lon_lan(user_id):
    # Search for a specific document
    query = {"_id": ObjectId(user_id)}
    user_object = collection.find_one(query)
    if user_object:
        # filter by location
        app = Nominatim(user_agent="test2")
        # address of user
        user_col = user_object['address'] #return {'street': '', 'city': '', 'state': 'CA', 'zip_code': '', 'country': 'USA'}
        if user_col['street']:
            user_add = user_col['street'] + ', ' + user_col['city'] + ', ' + user_col['state'] 
        else:
            user_add = user_col['city'] + ', ' + user_col['state'] 
        address = app.geocode(user_add).raw
        # get long and lat from data
        user_loc = [float(address['lat']), float(address['lon'])]
        new_data = {"user_loc": user_loc}
        collection.update_one(query, {"$set": new_data})
        print("Updated successfully")
    else:
        print(f"{user_id} doesn't exist")

#add_lon_lan('657245152201f887d4fa868a')
    