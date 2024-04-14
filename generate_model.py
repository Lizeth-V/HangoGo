#install all of these dependencies, 
#tensorflow however required me to change some paths in my windows machine

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

#import warnings
#warnings.filterwarnings("ignore", category=DeprecationWarning, module="tensorflow")
################################################################

import pandas as pd
import numpy as np
import time
################################################################

from pymongo import MongoClient
from bson import ObjectId
################################################################

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
################################################################


def generate_place_probabilities(uid):
    import tensorflow as tf

    start = time.time()

    #read in dataframe from the cleaned datafile
    place_df = pd.read_json('Hango.Places.json')
    print('Running time: ', int((time.time() - start) * 1000), 'ms')

    #where Nhu's subtype coding will go

    place_df.rename(columns={'_id': 'place_id'}, inplace=True)


    place_df['place_id'] = place_df['place_id'].apply(lambda x: x['$oid'])

    #print(place_df.head())
    ################################################################
    #ENCODE TYPES

    # Get unique subtypes
    unique_subtypes = set(subtype for sublist in place_df['sub_types'] for subtype in sublist)

    # Create a DataFrame with one-hot encoding columns for subtypes
    subtype_df = pd.DataFrame({subtype: place_df['sub_types'].apply(lambda x: 1 if subtype in x else 0) for subtype in unique_subtypes})

    # Concatenate the original DataFrame with the new subtype DataFrame
    place_df = pd.concat([place_df, subtype_df], axis=1)

    # Apply one-hot encoding to 'main_type' column
    place_df = pd.get_dummies(place_df, columns=['main_type'], prefix='main_type')

    # Drop the original 'sub_types' column if needed
    place_df = place_df.drop('sub_types', axis=1)
    #place_df = place_df.drop('main_type', axis=1)

    #place_df['age'] = place_df_features['age'].map({'Y': 1, 'N': 0})

    # Display the resulting DataFrame
    #place_df.head()
    #place_df.shape

    ################################################################
    #Build Ratings Matrix

    connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
    dbname = "Hango"
    collection_name = "ratings"

    client = MongoClient(connection_string)
    db = client[dbname]

    collection = db[collection_name]
    #reviewTable = pd.DataFrame()

    query = {'user_id': uid}

    review_table = list(collection.find(query))

    generated_reviews = pd.DataFrame(review_table)
    print('Running time: ', int((time.time() - start) * 1000), 'ms')

    #################################################################

    #merge the two dataframes based on the place id to generate factor matrix
    #drop features that are irrelevant to the model (distinction)

    #merged_df related to the ratings

    merged_df = pd.merge(generated_reviews, place_df, left_on='place_id', right_on='place_id', how='inner')

    place_df =  pd.merge(place_df, generated_reviews, left_on='place_id', right_on='place_id', how='outer', indicator=True)

    #this creates a list of places that the user hasn't reviewed
    unique_to_generated_reviews = place_df[place_df['_merge'] == 'left_only'].drop(columns=['_merge'])
    
    #drop irrelevant columns to the model
    merged_df = merged_df.drop(columns=['_id','user_id','place_id','name', 'address', 'weblink','price','age','timestamp'])

    #seperate the data fields from the field we need to predict (rating values)
    X = merged_df.drop(['feedback'], axis=1)
    y = merged_df['feedback']

    #split into test/train sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #Display the shapes of the resulting sets
    #print("Train set shape:", X_train.shape, y_train.shape)
    #print("Test set shape:", X_test.shape, y_test.shape)

    #standardize our data features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)


    #I was playinbg around i settled on 256 with a lot of layers bc we have like 300 ish features
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1, activation='sigmoid')
        ])

    #compile the model
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy'])

    #fit the model with the training data
    model.fit(X_train_scaled, y_train, epochs=10, batch_size=16, validation_split=0.2)

    #just for evaluation
    y_pred_proba = model.predict(X_test_scaled)
    y_pred = np.round(y_pred_proba)

    #turn to bin
    y_pred = y_pred.flatten().astype(int)

    #print accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)


    #drop unnecessary columns from place_df
    place_df_features = place_df.drop(columns=['address', 'weblink', 'price', 'age','timestamp', '_id', '_merge', 'feedback', 'user_id'])

    #standardize features
    place_df_features_scaled = scaler.transform(place_df_features.drop(columns=['place_id','name']))

    #feed the rest of the places intp the trained model to get the acceptance probs
    acceptance_probabilities = model.predict(place_df_features_scaled)

    #add it to the dataframe to order
    place_df_features['acceptance_probability'] = acceptance_probabilities

    #new df in order of acceptance probability
    top_locations = place_df_features.sort_values(by='acceptance_probability', ascending=False) 

    # Get all place IDs
    all_place_ids = set(top_locations['place_id'])

    # Get place IDs that the user has reviewed
    reviewed_place_ids = set(generated_reviews['place_id'])

    # Find the set difference to get place IDs that the user hasn't reviewed
    unreviewed_place_ids = all_place_ids - reviewed_place_ids

    #mongo upload into the user database as a list
    collection_name = "User Data"

    client = MongoClient(connection_string)
    db = client[dbname]

    collection = db[collection_name]

    try:
        collection.update_one(
        {"_id": ObjectId(uid)},
        {
            "$set": {
                "rec_probs": list(unreviewed_place_ids)
            }
        },
        upsert=True  #needed since users wont have the list until the first time they use the model
    )
        print("Update successful!")
    except Exception as e:
        print(f"Update failed: {e}")

    #entire runtime, for performance analysis
    print('Running time: ', int((time.time() - start) * 1000), 'ms')


#this is just for demoing
#generate_place_probabilities('6615b194f92286e38d5f91b2')