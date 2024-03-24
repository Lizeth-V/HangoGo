import requests
import googlemaps
import pandas as pd
import time

api_key = "AIzaSyDHkwv5g7hUxpT8YS2MfnxJguUc87babIc"
#base_url = "https://places.googleapis.com/v1/places:searchNearby"

map_client = googlemaps.Client(api_key)

places_to_add = [
    'Things to do',
    'Restaurants',
    'Malls',
    'Boba',
    'Cafe'
    'Museum',
    'Art',
    'Arcade',
    'Study'
]



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

def get_results_from_api(location, radius, keyword):
    # Create a list to store result types
    results_list = [] 
    next_page_token = None

    # Exclude certain types of places from the results
    # Hospitals and businesses that are not designed for hanging out
    exclude_keywords = ['lodging', 'doctor', 'insurance', 'local_government_office', 'car_dealer', 'car_repair', 'hospital']

    # Include keywords for boba shops and cafes
    include_keywords = ['boba', 'cafe']

    # Call API to store results by passing in parameters
    response = map_client.places_nearby(
        location=location, 
        radius=radius,
        keyword=keyword,
    ) 

    
    # Append results to the results list
    results_list.extend(response.get('results'))
    next_page_token = response.get('next_page_token')

    # The following allows us to continuously get results.
    # It works like a Google search with results per pages.
    # Thus, we have to sequentially go through pages and continue
    # To store results
    while next_page_token:
        #Have to sleep for api requests
        time.sleep(2)   

        #Just for visuals sake...
        print('Gathering results...')

        response = map_client.places_nearby(
            location=location, 
            radius=radius,
            keyword=keyword,  # Include multiple keywords
            page_token=next_page_token,
        ) 

        # Append results to the results list
        results_list.extend(response.get('results'))
        next_page_token = response.get('next_page_token') if 'next_page_token' in response else None  # Update next_page_token for the next iteration
        
    return results_list    #Create a list to store result types
   
################################################################

#Add results from each location and type to a list 
places_list = []
for types in places_to_add:
    for location in locations:
        places_list = places_list + get_results_from_api(location=location, radius=radius, keyword = types)

################################################################

#Create a dataframe for total results and modify the data
places_df = pd.DataFrame(places_list)

#Extract Latitude and longitude and rename the address
places_df['latitude'] = places_df['geometry'].apply(lambda x: x['location']['lat'])
places_df['longitude'] = places_df['geometry'].apply(lambda x: x['location']['lng'])
places_df['google_address'] = 'https://www.google.com/maps/place/?q=place_id:' + places_df['place_id']
places_df.rename(columns= {'vicinity':'address'})

#Drop irrelevant or non-uniform data
columns_to_drop = ['icon','icon_mask_base_uri','business_status','icon_background_color',
                   'opening_hours', 'scope', 'plus_code','place_id','geometry'] 

for column in columns_to_drop:
    places_df = places_df.drop(column, axis=1)

################################################################

# Print the DataFrame
excel_filename = "places_data.xlsx"
places_df.to_excel(excel_filename, index=False)

print(f"Data has been saved to {excel_filename}")


#For inserting into database
data_to_insert = {
    "name": '',
    "latitude":'',
    "longitude": '',
    "address": '',
    "categories": '',
    "rating": '',
    "rating_amount": '',
    "photolink": '',
}