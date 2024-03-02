#install all of these dependencies, 
#tensorflow however required me to change some paths in my windows machine

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

#import warnings
#warnings.filterwarnings("ignore", category=DeprecationWarning, module="tensorflow")
################################################################
import tensorflow as tf

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


def generate_place_probablities(uid):
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

    # Rows unique to generated_reviews
    unique_to_generated_reviews = place_df[place_df['_merge'] == 'left_only'].drop(columns=['_merge'])

    # Display or use the unique rows as needed
    #print(unique_to_generated_reviews)
    #print(merged_df)       

    merged_df = merged_df.drop(columns=['_id','user_id','place_id','name', 'address', 'weblink','price','age','timestamp'])

    print('Running time: ', int((time.time() - start) * 1000), 'ms')

    # Display the combined dataset
    #print(merged_df.head())
    #print(merged_df.size)

    #print(place_df.head)


    #split the data into test/train


    # Extract features (X) and target variable (y)
    X = merged_df.drop(['feedback'], axis=1)
    y = merged_df['feedback']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Display the shapes of the resulting sets
    #print("Train set shape:", X_train.shape, y_train.shape)
    #print("Test set shape:", X_test.shape, y_test.shape)

    # Standardize features (optional but often recommended for neural networks)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    '''model = tf.keras.Sequential([
        tf.keras.layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),  # Additional layer
        tf.keras.layers.Dense(8, activation='relu'),   # Additional layer
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])'''

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1, activation='sigmoid')
        ])

    # Compile the model with a lower learning rate
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

    # Train the model on the training set
    model.fit(X_train_scaled, y_train, epochs=10, batch_size=16, validation_split=0.2)

    # Evaluate the model on the test set
    y_pred_proba = model.predict(X_test_scaled)
    y_pred = np.round(y_pred_proba)

    # Convert predictions to binary (0 or 1)
    y_pred = y_pred.flatten().astype(int)

    # Evaluate the performance of the model
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    # Display additional metrics if needed
    #print("Classification Report:\n", classification_report(y_test, y_pred))

    # Drop unnecessary columns from place_df
    place_df_features = place_df.drop(columns=['address', 'weblink', 'price', 'age','timestamp', '_id', '_merge', 'feedback', 'user_id'])

    #STandardize here with drop
    # Standardize features
    place_df_features_scaled = scaler.transform(place_df_features.drop(columns=['place_id','name']))

    # Use the trained model to predict acceptance probabilities
    acceptance_probabilities = model.predict(place_df_features_scaled)

    # Add the predicted probabilities to place_df_features
    place_df_features['acceptance_probability'] = acceptance_probabilities

    # Sort by acceptance probability in descending order
    top_locations = place_df_features.sort_values(by='acceptance_probability', ascending=False) 


    collection_name = "User Data"

    client = MongoClient(connection_string)
    db = client[dbname]

    collection = db[collection_name]

    try:
        collection.update_one(
        {"_id": ObjectId(uid)},
        {
            "$set": {
                "rec_probs": top_locations['place_id'].head(10).tolist()
            }
        },
         upsert=True  # This will insert a new document if it doesn't exist

    )
        print("Update successful!")
    except Exception as e:
        print(f"Update failed: {e}")


    # Display the top locations
    #print(top_locations[['place_id', 'name', 'acceptance_probability']].head(20))
    print('Running time: ', int((time.time() - start) * 1000), 'ms')

def main():
    generate_place_probablities('6568cbef4a9658311b3ee704')

main()