import tensorflow as tf
import pandas as pd
import keras
import random
from pymongo import MongoClient
from bson import ObjectId
from scipy.spatial.distance import cosine
import math

connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
collection_name = "Places"

client = MongoClient(connection_string)
db = client["Hango"]
collection_name = "User Data"
collection = db[collection_name]

#return user information from database (USE WHEN INITIAL PAGE IS FINISHED)
#Aidan's code
def get_user_from_id(user_id): 
    query = {"_id": ObjectId(user_id)}
    user_object = collection.find_one(query)
    if user_object:
        return user_object

#return df with places that meet the criteria (and dropping unnecessary data)
def df_meet_criteria(user_object, lat, long):
    ### read in dataframe from the cleaned datafile ###
    df = pd.read_json('Hango.Places.json')

    ### convert object id to str (Aidan's code) ###
    df.rename(columns={'_id': 'place_id'}, inplace=True)
    df['place_id'] = df['place_id'].apply(lambda x: x['$oid'])

    ### filter by age, main_type, and location (reduce calculations) ###
    age = user_object['age']
    main_type = user_object['interests']
    for i in range(len(main_type)):
        main_type[i] = main_type[i][0].upper() + main_type[i][1:].lower()
    
    # N means age doesn't matter, Y means age does matter
    # if underage, only keep the ones with N as age
    if age < 21:
        df = df[df['age'] == 'N']
    
    # only keep the main_types in df that are main_type
    df = df[df['main_type'].isin(main_type)]
    
    # filter by location
    #query = { "_id": user_object['_id'] }
    #user_loc = collection.find_one(query)['user_loc'] #return lat and long
    user_loc = [lat, long]
    # get radius
    radius = 7/111 # radius of 10 miles to get enough places for initial recommendations
    # find radius in context of user lat and lon
    lat_least = user_loc[0]-radius
    lat_most = user_loc[0]+radius
    lon_least = user_loc[1]-radius
    lon_most = user_loc[1]+radius
    # only keep the ones within radius
    lat_radius = (df['lat'] >= lat_least) & (df['lat'] <= lat_most)
    df = df[lat_radius]
    lon_radius = (df['lon'] >= lon_least) & (df['lon'] <= lon_most)
    df = df[lon_radius]
    
    # then drop it from the df (unnecessary)
    df.drop(columns=['main_type', 'weblink', 'age'], inplace=True)

    #remove places that have the same name but different locations (only keep the one that is closest to user location)
    #pythagorean theorem c = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    grouped = df.groupby('name')
    removeList = []
    d = {}
    for name, group in grouped:
        if len(group) > 1:  # Only print if there are multiple rows with the same name
            for index, row in group.iterrows():
                distance = math.sqrt((row['lat']-user_loc[0])**2 + (row['lon']-user_loc[1])**2)
                d[distance] = index
            sorted_d = dict(sorted(d.items()))
            while len(sorted_d) > 1:
                removeList.append(sorted_d.popitem()[1])
                d.popitem()
            d.popitem()
    df = df.drop(removeList)
    df.drop(columns=['lat', 'lon'], inplace=True)
    return df

def recommendPlaces(user_ID, places_list):
    already_rec_collection = db["ratings"]
    query_ratings = {"user_id": user_ID}
    places = list(already_rec_collection.find(query_ratings))
    #list of place_ids in the rating database to check with the result_list
    check = [place['place_id'] for place in places]
    #remove places that are already in the check list
    for place in places_list[:]: #prevent length of list decreasing and not being able to delete
        if place in check:
            places_list.remove(place) 
    #return place for app
    if len(places_list)>0:
        choice = random.choice(places_list)
        places_collection = db["Places"]
        query = {"_id": ObjectId(choice)}
        output = places_collection.find_one(query)
        return output

def get_one_initial_recommend(user_id, lat, long):
    ### extract user info to generate filtered df with only relevant places ###
    user_object = get_user_from_id(user_id)
    df = df_meet_criteria(user_object, lat, long)

    ### STEP 1: hot-encode ###
    # get unique subtypes (Aidan's code)
    unique_subtypes = set(subtype for sublist in df['sub_types'] for subtype in sublist)
    # create a DataFrame with one-hot encoding columns for subtypes (Aidan's code)
    subtype_df = pd.DataFrame({subtype: df['sub_types'].apply(lambda x: 1 if subtype in x else 0) for subtype in unique_subtypes})
    # concatenate the original DataFrame with the new subtype DataFrame (Aidan's code)
    df = pd.concat([df, subtype_df], axis=1)
    # drop original sub_types (unnecessary)
    df.drop(columns='sub_types', inplace=True)

    ### STEP 2: get averaged rating from the df ###
    # use Bayesian average rating formula to make sure rating isn't inflated (from too little ratings)
    C = df['rating'].mean()  # get avg rating of all ratings
    m = df['rating_amount'].quantile(0.9)  # get quantile threshold for rating amount (basically removes the one with too little ratings in calculation)
    df['weighted_rating'] = ((df['rating_amount'] / (df['rating_amount'] + m)) * df['rating'] + (m / (df['rating_amount'] + m)) * C).round(2)
    # then drop rating and rating_amount from df
    df.drop(columns=['rating', 'rating_amount'], inplace=True)

    ### STEP 3: sort average rated df from best to least
    df.sort_values(by='weighted_rating', ascending=False, inplace=True)
    #using best rated first
    distance_df = df.drop(columns=['place_id', 'name', 'address', 'price', 'weighted_rating'])
    best = distance_df.iloc[0]
    distance_df.drop(distance_df.index[0], inplace=True)

    ### STEP 4: using best rated place from the df, calculate 5 that are best similar and 5 that are least similar 
    # for our users to initally rate and build their profile ###
    # subtract avg from list to ensure that missing values or 0's don't affect the distance 
    mean_best = best.mean()
    best = best * mean_best
    # get the cosine distance for each row (0 indicates that the vectors are perfectly similar (i.e., they point in the same direction). 
    # 1 indicates that the vectors are orthogonal (i.e., they are perpendicular to each other). 
    # and 2 indicates that the vectors are perfectly dissimilar (i.e., they point in opposite directions)).
    for index, row in distance_df.iterrows():
        mean_row = row.mean()
        row = row * mean_row
        cos_distance = cosine(best, row)
        distance_df.loc[index, 'distance'] = cos_distance
    distance_df.sort_values(by='distance', ascending=True, inplace=True)

    ### STEP 5: return the 10 places for user to rate (should allow for diverse ratings that emphasize user preferences) ###
    #the best rated place
    places_list = []
    best_index = best.name
    places_list.append(df.loc[best_index]['place_id'])
    #the most different place, least different place from rated first
    most_4_similar = distance_df.head(4)
    least_5_similar = distance_df.tail(5)
    #connect distance_df to original df to get place_id and name
    for index, row in most_4_similar.iterrows():
        places_list.append(df.loc[index]['place_id'])
    for index, row in least_5_similar.iterrows():
        places_list.append(df.loc[index]['place_id'])
    #print(str(user_object['_id']))
    place = recommendPlaces(str(user_object['_id']), places_list)
    return place