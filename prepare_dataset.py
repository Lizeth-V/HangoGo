#install all of these dependencies, 
#tensorflow however required me to change some paths in my windows machine

import tensorflow as tf
import pandas as pd
import keras
from keras.utils import FeatureSpace
import random

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

#merge the two dataframes based on the place id to generate factor matrix
#drop features that are irrelevant to the model (distinction)
merged_db = pd.merge(generated_reviews, df, left_on='place', right_on='place_id', how='inner')
merged_db = merged_db.drop(columns=['user_id','place_id','place', 'name', 'address', 'weblink','price'])

#For now I think, we might be overfitting with every amount of data
merged_db['sub_types'] = merged_db['sub_types'].apply(lambda x: x[:3] if isinstance(x, list) else x)
merged_db[['subtype_1', 'subtype_2', 'subtype_3']] = pd.DataFrame(merged_db['sub_types'].tolist(), index=merged_db.index)

# Drop the original 'sub_types' column if needed
merged_db = merged_db.drop(columns=['sub_types'])
    
# Display the combined dataset
print(merged_db.head())
print(merged_db.size)

#turn into datasets

#divide the data in 2 sets train and validation
val_dataframe = merged_db.sample(frac=0.2, random_state=1337)
train_dataframe = merged_db.drop(val_dataframe.index)

#divide into features and the output value
val_ds_y = val_dataframe['feedback']
train_ds_y = train_dataframe['feedback']

val_ds_x = val_dataframe.drop(['feedback'], axis=1)
train_ds_x = train_dataframe.drop('feedback', axis=1)



#pardon if this is changed in the future this is only a month old not much documentation on it ;-;
feature_space = FeatureSpace(
    features={
        
        #"price": "integer_categorical", ##NEEDS TO BE PREPROCESSED SOMETIMES DICT SOMETIMES NOT
        
        "main_type": "string_categorical",
        "sub_type_1": "string_categorical",
        "sub_type_2": "string_categorical",
        "sub_type_3": "string_categorical",
        "age": "string_categorical",
        
        #"u_age": "float_discretized",
        #I'm not sure if we can even use age to predict.
        
        #normalized stuff
        "lat": "float_normalized",
        "lon": "float_normalized",
        "rating": "float_normalized",
        "rating_amount": "float_normalized",
    },
    #We make features that depend on both im not certain how reliable this will be.
    crosses=[("lat", "lon"), ("rating", "rating_amount")],
    crossing_dim=32,
    
    output_mode="concat",
)


#Here are our test and validation sets ^
#Build the Model Below