import json
import pandas as pd

data = []
remove = ['Doctors', 'Health & Medical', 'Real Estate', 'Car Dealers', 'Furniture Rental', 'Child Care & Day Care', 'Convenience Stores', 'Fashion', 'Department Stores', 'Gyms', 'Event Planning & Services', 'Local Services', 'Limos', 'Taxis']

# extract data from json file & remove places from the remove list (the leftover ones after keeping)
with open('yelp_data.json', encoding="utf8") as f:
    places = json.load(f)
    for place in places:
        #del places["hours"]
        if place['categories'] and not any(category in place['categories'] for category in remove):
            data.append(place)

# add filter data into json file
with open('yelp_data.json', 'w') as f:
    json.dump(data, f)

# convert it into a csv for better readability in excel sheet
with open('yelp_data.json', encoding='utf-8') as f:
    df = pd.read_json(f)
df.to_csv('testv4.csv', encoding='utf-8', index=False)