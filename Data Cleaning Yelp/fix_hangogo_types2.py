import pandas as pd
import json

data = []

# extract data from json file & making sure there are no duplicate values like bakery vs bakeries, bookstore vs book_store (to make data more uniform)
with open('Hango.Places.json', encoding='utf-8') as f:
    places = json.load(f)
    for place in places:
        for i in range(len(place['sub_types'])):
            if place['sub_types'][i] == 'amusement_park' or place['sub_types'][i] == 'amusement_parks':
                place['sub_types'][i] = 'amusement_park'
            if place['sub_types'][i] == 'art_gallery' or place['sub_types'][i] == 'art_galleries':
                place['sub_types'][i] = 'art_gallery'
            if place['sub_types'][i] == 'bakery' or place['sub_types'][i] == 'bakeries':
                place['sub_types'][i] = 'bakery'
            if place['sub_types'][i] == 'bar' or place['sub_types'][i] == 'bars':
                place['sub_types'][i] = 'bar'
            if place['sub_types'][i] == 'book_store' or place['sub_types'][i] == 'bookstores':
                place['sub_types'][i] = 'bookstore'
            if place['sub_types'][i] == 'pet_store' or place['sub_types'][i] == 'pet_stores':
                place['sub_types'][i] = 'pet_store'
            if place['sub_types'][i] == 'museum' or place['sub_types'][i] == 'museums':
                place['sub_types'][i] = 'museum'
            if place['sub_types'][i] == 'restaurant' or place['sub_types'][i] == 'restaurants':
                place['sub_types'][i] = 'restaurant'
            if place['sub_types'][i] == 'zoo' or place['sub_types'][i] == 'zoos':
                place['sub_types'][i] = 'zoo'
        data.append(place)

# add filter data into json file
with open('Hango.Places.json', 'w') as f:
    json.dump(data, f)