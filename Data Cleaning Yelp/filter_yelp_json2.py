import json
import pandas as pd

data = []

# extract data from json file & only keep restaurants that are good for groups
with open('yelp_data.json', encoding="utf8") as f:
    places = json.load(f)
    for place in places:
        if place['attributes'] and "RestaurantsGoodForGroups" in place['attributes']:
            if place['attributes']["RestaurantsGoodForGroups"] == 'True':
               data.append(place)
        else:
           data.append(place)

# add filter data into json file
with open('yelp_data.json', 'w') as f:
    json.dump(data, f)

# convert it into a csv for better readability in excel sheet
with open('yelp_data.json', encoding='utf-8') as f:
    df = pd.read_json(f)
df.to_csv('testv3.csv', encoding='utf-8', index=False)