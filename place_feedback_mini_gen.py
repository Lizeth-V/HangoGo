import time
from pymongo import MongoClient
import geocoder
import random

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
        
        return result_list
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    client.close()



# Print the user ID if found
user_ID = sign_in_email()

if user_ID:
    user_loc = geocoder.ip('me').latlng
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

        feedback = input("'A' for accept, 'D' for decline: ")

        if feedback == 'A':
            temp_feedback.accept_recommendation_update(user_ID, place_ID)
        elif feedback == 'D':
            temp_feedback.decline_recommendation_update(user_ID, place_ID)
        else:
            print("Please enter a valid response: ")
            print("Place: ", str(choice['name']))
            print("Address: ", str(choice['address']))
            print("Main Type: ", str(choice['main_type']))
            print("Sub Types: ", str(choice['sub_types']))
            print("View on google: ", str(choice['weblink']))

            feedback = input("'A' for accept, 'D' for decline: ")

