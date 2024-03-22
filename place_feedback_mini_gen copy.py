import time
from pymongo import MongoClient
import geocoder
import random
from geopy.geocoders import Nominatim

import temp_feedback

def sign_in_email():
    email = input("Enter your email address: ")
    
    connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
    dbname = "Hango"
    collection_name = "User Data"

    client = MongoClient(connection_string)
    db = client[dbname]

    collection = db[collection_name]

    query = {"email": email}

    user_object = collection.find_one(query)

    if user_object:
        user_ID = str(user_object['_id'])
        return user_ID
    else:
        print("Check Spelling or email in the database.")
        return None
    
    client.close()

def generate_location(radius, user_location):
    connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
    dbname = "Hango"
    collection_name = "Places"

    client = MongoClient(connection_string)
    db = client[dbname]

    collection = db[collection_name]

    # Define the center point for the query
    center_point = {
        "lat": user_location[0],
        "lon": user_location[1]
    }

    # Define the query for locations within the specified range
    query = {
        "lat": {
            "$gte": center_point["lat"] - (radius / 111),  # Latitude is approx 111 km per degree
            "$lte": center_point["lat"] + (radius / 111)
        },
        "lon": {
            "$gte": center_point["lon"] - (radius / 111),  # Longitude varies, but this is a rough approximation
            "$lte": center_point["lon"] + (radius / 111)
        }
    }

    try:
        # Execute the query and store the results in a list
        result_list = list(collection.find(query))
        
        #NHU'S CODE START (prevent generating the same locations)
        #cross check results of list with ratings data
        already_rec_collection = db["ratings"]
        query_ratings = {"user_id": user_ID}
        places = list(already_rec_collection.find(query_ratings))
        #list of place_ids in the rating database to check with the result_list
        check = [place['place_id'] for place in places]
        #remove places that are already in the check list
        for place in result_list[:]: #prevent length of list decreasing and not being able to delete
            if str(place['_id']) in check:
                result_list.remove(place) 
        #NHU'S CODE END

        #NHU's CODE
        if len(result_list) == 0:
            print("No new places to recommend.")
        #END
            
        return result_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    client.close()



# Print the user ID if found
user_ID = sign_in_email()

if user_ID:
    #NHU'S CODE START (retrieve actual location from user in database and return long/lat for model)
    # Instantiate a new Nominatim client
    app = Nominatim(user_agent="test")
    # Address of user
    # query = { "_id": ObjectId(user_ID) }
    # user_col = collection.find_one(query)['address'] #return {'street': '', 'city': '', 'state': 'CA', 'zip_code': '', 'country': 'USA'}
    # user_add = user_col['street'] + ', ' + user_col['city'] + ', ' + user_col['state'] 
    user_add = str(input('Enter city (like Long Beach, CA): '))
    address = app.geocode(user_add).raw
    # Get long and lat from data
    user_loc = [float(address['lat']), float(address['lon'])]
    #NHU'S CODE END

    radius = float(input("Choose radius in mi: "))
    
    print("User: ", user_ID, "at " , user_loc[0], user_loc[1])

    place_list = generate_location(radius, user_loc)

    while len(place_list)>0:
        choice = random.choice(place_list)
        place_list.remove(choice)
        place_ID = str(choice['_id'])
        print("Place: ", str(choice['name']))
        print("Address: ", str(choice['address']))
        print("Main Type: ", str(choice['main_type']))
        print("Sub Types: ", str(choice['sub_types']))
        print("View on google: ", str(choice['weblink']))

        feedback = input("'A' for accept, 'D' for decline, 'E' to exit: ")

        if feedback == 'A':
            temp_feedback.accept_recommendation_update(user_ID, place_ID)
        elif feedback == 'D':
            temp_feedback.decline_recommendation_update(user_ID, place_ID)
        elif feedback == 'E':
            break
        else:
            print("Please enter a valid response: ")
            print("Place: ", str(choice['name']))
            print("Address: ", str(choice['address']))
            print("Main Type: ", str(choice['main_type']))
            print("Sub Types: ", str(choice['sub_types']))
            print("View on google: ", str(choice['weblink']))

            feedback = input("'A' for accept, 'D' for decline, 'E' to exit: ")

