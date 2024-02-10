import requests
import googlemaps
import pandas as pd
import time


api_key = ""
#base_url = "https://places.googleapis.com/v1/places:searchNearby"

map_client = googlemaps.Client(api_key)

food_to_add = [
    #Food Categories
    'food',
    'dining',
    'bakery',]
entertainment_to_add = [    
    #Entertainment Categories
    'entertainment',
    'arcade']
nature_rec_to_add = [
    #Nature/Recreation Categories
    'nature',
    'hike',
    'parks',
]
nightlife_to_add = [
    #Nightlife Categories
    'bar',
    'club',]
mus_art_to_add = [ 
    #Museum/Art Categories
    'museum',
    'art',
    'library',]
drinks_to_add = [    
    #Drinks Categories
    'cafe',
    'boba']

places_to_add = {
    'Food':food_to_add,
    'Drinks':drinks_to_add,
    'Museum/Art':mus_art_to_add,
    'Entertainment':entertainment_to_add,
    'Nature/Recreation':nature_rec_to_add,
    'Nightlife':nightlife_to_add
}

subtypes_mapping ={
    'bakery':'bakery',
    'cafe':'cafe',
    'food':'food',
    'restaurant':'restaurant',
    'store':'store',
    'museum':'None',
    'art_gallery':'art_gallery',
    'movie_theater':'movie_theater',
    'tourist_attraction':'tourist_attraction',
    'museum':'museum',
    'park':'park',
    'book_store':'book_store',
    'library':'library',
    'zoo':'zoo',
    'florist':'florist',
    'bar':'bar',
    'night_club':'night_club',
    'bowling_alley':'bowling_alley',
    'amusement_park':'amusement_park',
    'pet_store':'pet_store',
    'beauty_salon':'beauty_salon',
    'clothing_store':'clothing_store',
    'spa':'spa',
    'meal_takeaway':'meal_takeaway',
    'meal_delivery':'meal_delivery',

}

removal_mapping ={
    'finance',
    'health',
    'lodging',
    'school',
    'parking',
}

#We are just inflating the database with points of interest around the area.
#This is easily changed but we locate points around Long Beach 
#since we will only be able to test in the Southern California area.
#Place API limits us to at most 60 points of interest per request thus we
#will search multiple coords in the area.
locations = [
    # Los Angeles County
    "34.0522, -118.2437",  # Los Angeles Downtown
    "34.0227, -118.4956",  # Santa Monica
    "34.1478, -118.1445",  # Pasadena
    "33.7701, -118.1937",  # Long Beach
    "34.0900, -118.4065",  # Beverly Hills
    "34.1425, -118.2551",  # Glendale

    # Orange County
    "33.6846, -117.8265",  # Irvine
    "33.8366, -117.9143",  # Anaheim
    "33.6603, -117.9992",  # Huntington Beach
    "33.6189, -117.9289",  # Newport Beach
    "33.5427, -117.7854",  # Laguna Beach
    "33.6412, -117.9187",  # Costa Mesa
]


#This is not 100% accurate conversion but close enough to search in the miles radius
def mi_2_meters(miles):
    return miles*1609

#This is measured in meters
radius = mi_2_meters(10)  #in meters adjust as needed


def get_results_from_api(location, radius, place_type):
    c = 0
    for keyword in places_to_add[place_type]:
        # Create a list to store result types
        results_list = [] 
        next_page_token = None

        print('Gathering results...',keyword,location)

        # Call API to store results by passing in parameters
        response = map_client.places_nearby(
            location=location, 
            radius=radius,
            keyword=keyword,
        ) 

        # Append results to the results list adding the main type as a category
        for item in response.get('results'):
            if place_type == 'Nightlife': item['age'] = 'Y'
            else: item['age'] = 'N'


            tempSubtypes = []
            for sub_type in item['types']:
                if sub_type in subtypes_mapping:
                    tempSubtypes.append(subtypes_mapping[sub_type])
                elif sub_type in removal_mapping:
                    continue
            
            if keyword not in tempSubtypes:
                tempSubtypes.append(keyword)

            item['sub_types']=tempSubtypes
            item['main_type']=place_type
            results_list.append(item)

        c+=1
        next_page_token = response.get('next_page_token')

        # The following allows us to continuously get results.
        # It works like a Google search with results per pages.
        # Thus, we have to sequentially go through pages and continue
        # To store results
        while next_page_token and c < 3:
            #Have to sleep for api requests
            time.sleep(2)   

            #Just for visuals sake...
            print('Gathering results...',keyword,location)

            response = map_client.places_nearby(
                location=location, 
                radius=radius,
                keyword=keyword,  # Include multiple keywords
                page_token=next_page_token,
            )
            c+=1


            # Append results to the results list adding the main type as a category
        for item in response.get('results'):
            if place_type == 'Nightlife': item['age'] = 'Y'
            else: item['age'] = 'N'


            tempSubtypes = []
            for sub_type in item['types']:
                if sub_type in subtypes_mapping:
                    tempSubtypes.append(subtypes_mapping[sub_type])
                elif sub_type in removal_mapping:
                    continue

            if keyword not in tempSubtypes:
                tempSubtypes.append(keyword)
                
            item['sub_types']=tempSubtypes
            item['main_type']=place_type
            results_list.append(item)

            next_page_token = response.get('next_page_token') if 'next_page_token' in response else None  # Update next_page_token for the next iteration
        
        return results_list    #Create a list to store result types
   
################################################################

#Add results from each location and type to a list 
places_list = []
for types in places_to_add:
    for location in locations:
        places_list = places_list + get_results_from_api(location=location, radius=radius, place_type=types)

################################################################

#Create a dataframe for total results and modify the data
places_df = pd.DataFrame(places_list)

#Extract Latitude and longitude and rename the address
places_df['lat'] = places_df['geometry'].apply(lambda x: x['location']['lat'])
places_df['lon'] = places_df['geometry'].apply(lambda x: x['location']['lng'])
places_df['google_address'] = 'https://www.google.com/maps/place/?q=place_id:' + places_df['place_id']
places_df.rename(columns= {'vicinity':'address'},inplace=True)

#Drop irrelevant or non-uniform data
columns_to_drop = ['icon','icon_mask_base_uri','business_status','icon_background_color',
                   'opening_hours', 'scope', 'plus_code','place_id','geometry','permanently_closed'] 

places_df = places_df.drop(columns=columns_to_drop)

################################################################

# Print the DataFrame
#excel_filename = "places_data.xlsx"
#places_df.to_excel(excel_filename, index=False)

#
# print(f"Data has been saved to {excel_filename}")


################################################################################################
#MONGO DB STUFF
from pymongo import MongoClient, ASCENDING, errors

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


for index, row in places_df.iterrows():
    #For inserting into database, use names specified by the database schema
    data_to_insert = {
        "name": row['name'],
        "lat": row['lat'],
        "lon": row['lon'],
        "address": row['address'],
        "main_type": row['main_type'],
        "sub_types": row['sub_types'],
        "rating": row['rating'],
        "rating_amount": row['user_ratings_total'],
        "age": row['age'],
        "price": row['price_level'],
        #"from": 'google', #might be useful to know where its from, no useability other than knowing.
        "weblink": row['google_address'],
    }

    try: #running into a error that prevents inserts from proceeding if duplicates so we have to catch the errors.
        result = collection.insert_one(data_to_insert)
        print(f"Insert successful for {row['name']}")
    except errors.DuplicateKeyError:
        print(f"Duplicate key error. Skipping insertion for {row['name']}")
        continue
