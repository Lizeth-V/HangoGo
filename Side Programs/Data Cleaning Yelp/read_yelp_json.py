import json
import pandas as pd

data = []

# extract data from yelp
with open('yelp_academic_dataset_business.json', encoding="utf8") as f:
   for line in f:
        place = json.loads(line)
        # only keep the places that are in California
        if place.get('state') == 'CA':
            #remove business_id (don't need)
            del place["business_id"]
            data.append(place)

# put all of the CA places into a new JSON file (for more filtering later)
with open('yelp_data.json', 'w') as f:
    json.dump(data, f)

# convert it into a csv for better readability in excel sheet
with open('yelp_data.json', encoding='utf-8') as f:
    df = pd.read_json(f)
df.to_csv('test.csv', encoding='utf-8', index=False)