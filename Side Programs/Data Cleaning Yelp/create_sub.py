import json
import pandas as pd

data = []

# extract data from json file & make new sub categories such as age and sub_types
with open('yelp_data3.json', encoding="utf8") as f:
    places = json.load(f)
    for place in places:
        if 'Nightlife' in place["categories"]:
            place["age"] = "Y"
        else:
            place["age"] = "N"
        data.append(place)

with open('yelp_data3.json', 'w') as f:
    json.dump(data, f)

# convert it into a csv for better readability in excel sheet
with open('yelp_data3.json', encoding='utf-8') as f:
    df = pd.read_json(f)
df.to_csv('testv6.csv', encoding='utf-8', index=False)