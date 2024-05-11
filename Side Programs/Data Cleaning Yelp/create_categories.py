import json
import pandas as pd

data = []

# extract data from json file & make a new category called 'main_type' for each json object depending on the place category
with open('yelp_data2.json', encoding="utf8") as f:
    places = json.load(f)
    for place in places:
        if 'main_type' in place:
            #place["main_type"] = 'Nature/Recreation'
            data.append(place)

# create a new json file after cleaning
with open('yelp_data2.json', 'w') as f:
    json.dump(data, f)

# convert it into a csv for better readability in excel sheet
with open('yelp_data2.json', encoding='utf-8') as f:
    df = pd.read_json(f)
df.to_csv('testv5.csv', encoding='utf-8', index=False)