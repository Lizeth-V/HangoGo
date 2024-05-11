import pandas as pd
import json

data = []

# extract data from json file & make all the strings in sub_types all the same case and without space (to make data more uniform)
with open('Hango.Places.json', encoding='utf-8') as f:
    places = json.load(f)
    for place in places:
        new_sub = []
        for i in place['sub_types']:
            i = i.lower()
            i = i.replace(" ", "_")
            new_sub.append(i)
        place['sub_types'] = new_sub
        data.append(place)

# add filter data into json file
with open('Hango.Places.json', 'w') as f:
    json.dump(data, f)