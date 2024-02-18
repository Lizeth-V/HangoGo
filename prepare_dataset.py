import tensorflow as tf
import pandas as pd
import keras
from keras.utils import FeatureSpace
import random
#Libraries

#read in dataframe from the cleaned datafile
df = pd.read_json('Hango.Places.json')

subtypes = set()

for sub_types_list in df['sub_types']:
    for subtype in sub_types_list:
        subtypes.add(subtype)

df.rename(columns={'_id': 'place_id'}, inplace=True)

df['place_id'] = df['place_id'].apply(lambda x: x['$oid'])


df.head()


userdata ={
  "_id": {
    "$oid": "6567dcefba91df16f20f718d"
  },
  "username": "john_doe",
  "full_name": "John Doe",
  "email": "john@example.com",
  "age": 30,
  "address": {
    "street": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "zip_code": "12345",
    "country": "USA"
  }
}

#This is a function that builds fake reviews.
#We have no data due to a cold start so we need to create artificial feedback
def generateFakeReviews(id,age):
    
    reviewTable = pd.DataFrame()

    #This chooses 100 random places to give positive implicit feedback
    #Put into a temporary table

    #Change k to change amount
    positive_choices = random.sample(df['place_id'].tolist(), k=100)
    positive_reviews = [{'user_id': id, 'u_age': age, 'place': place, 'feedback': 1} for place in positive_choices]
    
    #This chooses 75 random places to give negative implicit feedback
    #Put into a temporary table

    #Change k to change amount
    negative_choices = random.sample(df['place_id'].tolist(), k=75)
    negative_reviews = [{'user_id': id, 'u_age': age, 'place': place, 'feedback': 0} for place in negative_choices]
    
    #append both to the temporary review table and return it
    reviewTable = reviewTable.append(positive_reviews, ignore_index=True)
    reviewTable = reviewTable.append(negative_reviews, ignore_index=True)

    return reviewTable

# Example usage
#age = 25 Need to figure out how this can help in content based filtering

#temp user id for programming and testing
uid = '6567dcefba91df16f20f718d'

#generate the fake review table
#keep age in it for now
generated_reviews = generateFakeReviews(id=uid, age=25)

generated_reviews.head(100)