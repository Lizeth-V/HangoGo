import requests
import googlemaps
import pandas as pd

api_key = "AIzaSyDHkwv5g7hUxpT8YS2MfnxJguUc87babIc"
#base_url = "https://places.googleapis.com/v1/places:searchNearby"

map_client = googlemaps.Client(api_key)


location = "33.770050,-118.193740"  #Long Beach for now
radius = 1000  #in meters adjust as needed

placesList = [] #list of places

response = map_client.places_nearby(
    location = location, 
    radius = radius,
    type='point_of_interest'
) #api call for nearby search 

results_list = response.get('results', []) #store results from api call into a list

# Create a DataFrame from the list of places
places_df = pd.DataFrame(results_list)

places_df = places_df[~places_df['types'].apply(lambda x: 'lodging' in x)]

columns_to_drop = ['icon','icon_mask_base_uri','business_status','icon_background_color']  # Adjust the column name as needed

for column in columns_to_drop:
    places_df = places_df.drop(column, axis=1)

# Print the DataFrame
excel_filename = "places_data.xlsx"
places_df.to_excel(excel_filename, index=False)

print(f"Data has been saved to {excel_filename}")

data_to_insert = {
    "place_name": '',
    "lat_long": '',
    "address": '',
    "types": '',
    "rating": '',
    "rating_amount": '',
    "photos": '',
}