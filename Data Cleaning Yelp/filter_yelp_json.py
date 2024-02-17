import json
import pandas as pd

data = []
keep = ['Restaurants', 'Food', 'Rental', 'Active Life', 'Arts & Entertainment', 'Bars', 'Coffee & Tea', 'Bikes'] #keep track of all categories that were removed iteratively

# extract data from json file & only keep categories specified in the keep list
with open('yelp_data.json', encoding="utf8") as f:
    places = json.load(f)
    for place in places:
       if place['categories'] and any(category in place['categories'] for category in keep):
          data.append(place)

# add filter data into json file
with open('yelp_data.json', 'w') as f:
   json.dump(data, f)

# convert it into a csv for better readability in excel sheet
with open('yelp_data.json', encoding='utf-8') as f:
    df = pd.read_json(f)
df.to_csv('testv2.csv', encoding='utf-8', index=False)
    

