from geopy.geocoders import Nominatim
from pymongo import MongoClient
from bson import ObjectId

connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
client = MongoClient(connection_string)
db = client["Hango"]
collection_name = "Location"
collection = db[collection_name]

# add a new field, lon_lan, to user by taking their location
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
        client.close()

        print("Updated successfully")
    else:
        print(f"{user_id} doesn't exist")

# take the list of cities to generate lon, lang (to use for chatbox)
def insert_lon_lan(cities):
    # insert each city into database after converting address to long and lang
    for city in cities:
        app = Nominatim(user_agent="test2")
        # address
        address = city + ", CA"
        address = app.geocode(address).raw
        # get long and lat from address
        coordinates = [float(address['lat']), float(address['lon'])]
        document = {
            "Name": city,
            "Coordinates": coordinates
        }
        # insert the document into the collection
        result = collection.insert_one(document)
        client.close()

        print(result)

cities = ["Aliso Viejo", "Anaheim", "Brea", "Buena Park", "Costa Mesa", "Cypress", "Dana Point", "Fountain Valley", "Fullerton", "Garden Grove", "Huntington Beach", "Irvine", "La Habra", "La Palma", "Laguna Beach", "Laguna Niguel", "Laguna Woods", "Lake Forest", "Los Alamitos", "Mission Viejo", "Newport Beach", "Orange", "Placentia", "Rancho Santa Margarita", "San Clemente", "San Juan Capistrano", "Santa Ana", "Seal Beach", "Stanton", "Tustin", "Villa Park", "Westminster", "Yorba Linda", "Agoura Hills", "Alhambra", "Arcadia", "Artesia", "Avalon", "Azusa", "Baldwin Park", "Bell", "Bell Gardens", "Bellflower", "Beverly Hills", "Bradbury", "Burbank", "Calabasas", "Carson", "Cerritos", "City of Industry", "Claremont", "Commerce", "Compton", "Covina", "Cudahy", "Culver City", "Diamond Bar", "Downey", "Duarte", "El Monte", "El Segundo", "Gardena", "Glendale", "Glendora", "Hawaiian Gardens", "Hawthorne", "Hermosa Beach", "Hidden Hills", "Huntington Park", "Inglewood", "Irwindale", "La Cañada Flintridge", "La Habra Heights", "La Mirada", "La Puente", "La Verne", "Lakewood", "Lancaster", "Lawndale", "Lomita", "Long Beach", "Los Angeles", "Lynwood", "Malibu", "Manhattan Beach", "Maywood", "Monrovia", "Montebello", "Monterey Park", "Norwalk", "Palmdale", "Palos Verdes Estates", "Paramount", "Pasadena", "Pico Rivera", "Pomona", "Rancho Palos Verdes", "Redondo Beach", "Rolling Hills", "Rolling Hills Estates", "Rosemead", "San Dimas", "San Fernando", "San Gabriel", "San Marino", "Santa Clarita", "Santa Fe Springs", "Santa Monica", "Sierra Madre", "Signal Hill", "South El Monte", "South Gate", "South Pasadena", "Temple City", "Torrance", "Vernon", "Walnut", "West Covina", "West Hollywood", "Westlake Village", "Whittier"]

insert_lon_lan(cities)
    