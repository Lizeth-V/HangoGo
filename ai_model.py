import pandas as pd

with open('Hango.Places.json', encoding='utf-8') as f:
    df = pd.read_json(f)
df = df.drop(columns=["weblink", "name", "address"])
df['main_type'] = pd.factorize(df['main_type'])[0] + 1

for types in df['sub_types']:
    print(types)
    print(pd.factorize(types)[0])