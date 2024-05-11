import pandas as pd


df = pd.read_json('Hango.Places.json')

#generate list of unique values of sub_types to encode later
subtypes = set()
for sub_types_list in df['sub_types']:
    for subtype in sub_types_list:
        subtypes.add(subtype)

print(list(subtypes))