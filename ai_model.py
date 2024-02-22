import pandas as pd
import numpy as np

# extract data from database json & drop irrelevant columns to start training
with open('Hango.Places.json', encoding='utf-8') as f:
    df = pd.read_json(f)
df = df.drop(columns=["weblink", "name", "address"])
# encode our categories (our labels) as numerical representation instead of strings
df['main_type'] = pd.factorize(df['main_type'])[0]

# encode our sub categories as numerical representation instead of strings (all_sub list comes from create_sublist.py)
all_sub = ['transportation', 'meal_delivery', 'wholesale_stores', 'american_(new)', 'drugstores', 'whale_watching_tours', 'skate_parks', 'home_&_garden', 'parks', 'swimming_pools', 'bookstore', 'rv_parks', 'empanadas', 'country_clubs', 'butcher', 'amusement_park', 'cinema', 'snorkeling', 'mountain_biking', 'desserts', 'himalayan/nepalese', 'bowling_alley', 'restaurant', 'beauty_salon', 'pop-up_shops', 'hot_dogs', 'internet_cafes', 'live/raw_food', 'drive-in_theater', 'modern_european', 'fishing', 'souvenir_shops', 'contractors', 'tanning', 'comedy_clubs', 'chicken_wings', 'food_trucks', 'sailing', 'coffee_&_tea', 'dim_sum', 'specialty_food', 'bike_rentals', 'bar', 'used_bookstore', 'seafood_markets', 'hot_pot', 'taiwanese', 'new_mexican_cuisine', 'wine_&_spirits', 'meat_shops', 'trainers', 'books', 'aquariums', 'motorcycle_rental', 'pakistani', 'cafeteria', 'airlines', 'herbs_&_spices', 'tea_rooms', 'ethnic_grocery', 'arts_&_crafts', 'speakeasies', 'arts_&_entertainment', 'basque', 'beverage_store', 'music_venues', 'farms', 'brazilian', 'lakes', 'rv_rental', 'patisserie/cake_shop', 'pool_halls', 'art_supplies', 'food_court', 'pizza', 'karaoke', 'outdoor_gear', 'zoo', 'wine_tours', 'olive_oil', 'vietnamese', 'bakery', 'fruits_&_veggies', 'asian_fusion', 'boating', 'hot_tub_&_pool', 'farmers_market', 'flowers_&_gifts', 'coffee_roasteries', 'sporting_goods', 'store', 'tacos', 'french', 'music_&_video', 'szechuan', 'pasta_shops', 'steakhouses', 'hiking', 'vegan', 'architectural_tours', 'food_delivery_services', 'archery', 'local_flavor', 'german', 'travel_services', 'ethnic_food', 'indonesian', 'carousels', 'kitchen_&_bath', 'gastropubs', 'spa', 'juice_bars_&_smoothies', 'beer_bar', 'surfing', 'videos_&_video_game_rental', 'paragliding', 'day_spas', 'golf_equipment', 'fish_&_chips', 'middle_eastern', 'dog_parks', 'professional_services', 'self-defense_classes', 'rafting/kayaking', 'keys_&_locksmiths', 'dive_bars', 'gift_shops', 'soup', 'seafood', 'hotels_&_travel', 'virtual_reality_centers', 'australian', 'mongolian', 'nature', 'coffeeshops', 'fitness_&_instruction', 'arabic', 'sandwiches', 'aerial_fitness', 'kombucha', 'diners', 'golf_lessons', 'food_tours', 'tex-mex', 'tapas_bars', 'yoga', 'skating_rinks', 'food', 'bus_tours', 'jazz_&_blues', 'acai_bowls', 'distilleries', 'antiques', 'music_&_dvds', 'moroccan', 'shaved_ice', 'guns_&_ammo', 'public_markets', 'dance_clubs', 'barbeque', 'donuts', 'beauty_&_spas', 'kickboxing', 'ramen', 'pop-up_restaurants', 'library', 'pool_cleaners', 'toy_stores', 'brewpubs', 'boxing', 'garage_door_services', 'car_rental', 'nurseries_&_gardening', 'soul_food', 'halal', 'belgian', 'irish_pub', 'breweries', 'shopping_centers', 'night_club', 'livestock_feed_&_supply', 'hang_gliding', 'poke', 'batting_cages', 'cosmetics_&_beauty_supply', 'irish', 'caribbean', 'park', 'karate', 'cafes', 'appliances', 'cheesesteaks', 'massage', 'american_(traditional)', 'fitness/exercise_equipment', 'discount_store', 'cupcakes', 'pet_sitting', 'pilates', 'korean', 'champagne_bars', 'delis', 'pets', 'active_life', 'shopping', 'bikes', 'horseback_riding', 'kids_activities', 'hookah_bars', 'tabletop_games', 'cocktail_bars', 'hong_kong_style_cafe', 'hunting_&_fishing_supplies', 'food_stands', 'cantonese', 'summer_camps', 'chicken_shop', 'piano_bars', 'gay_bars', 'lebanese', 'fondue', 'tours', 'home_services', 'vegetarian', 'pet_store', 'indian', 'bagels', 'sports_bars', 'health_markets', 'historical_tours', 'buffets', 'turkish', 'atv_rentals/tours', 'cheese_shops', 'cajun/creole', 'custom_cakes', 'japanese', 'beer', 'florist', 'lounges', 'barbers', 'ticket_sales', 'tobacco_shops', 'florists', 'spiritual_shop', 'beaches', 'nightlife', 'cideries', 'mags', 'cuban', 'soccer', 'do-it-yourself_food', 'breakfast_&_brunch', 'building_supplies', 'wine_bars', 'playgrounds', 'csa', 'club_crawl', 'tapas/small_plates', 'cardio_classes', 'boot_camps', 'pool_&_hot_tub_service', 'campgrounds', 'entertainment', 'tourist_attraction', 'hobby_shops', 'candy_stores', 'paddleboarding', 'chocolatiers_&_shops', 'gelato', 'wineries', 'sushi_bars', 'golf_equipment_shops', 'home_decor', 'wine_tasting_room', 'fast_food', 'creperies', 'comfort_food', 'tuscan', 'ice_cream_&_frozen_yogurt', 'festivals', 'international_grocery', 'imported_food', 'thai', 'mediterranean', 'tennis', 'dance_studios', 'museum', 'professional_sports_teams', 'clothing_store', 'macarons', 'video_game_stores', 'pet_services', 'cafe', 'british', 'noodles', 'gun/rifle_ranges', 'recreation_centers', 'scooter_rentals', 'beer_tours', 'pretzels', 'chinese', 'electronics', 
'burgers', 'organic_stores', 'peruvian', 'stadiums_&_arenas', 'wraps', 'barre_classes', 'performing_arts', 'beer_gardens', 'martial_arts', 'art_gallery', 'southern', 'meal_takeaway', 'italian', 'gluten-free', 'mexican', 'skydiving', 'salad', 'sports_clubs', 'latin_american', 'races_&_competitions', 'whiskey_bars', 'escape_games', 'grocery', "children's_museums", 'brazilian_jiu-jitsu', 'social_clubs', 'spanish', 'amateur_sports_teams', 'movie_theater', 'delicatessen', 'cycling_classes', 'pan_asian', 'bubble_tea', 'beach_equipment_rentals', 'scandinavian', 'falafel', 'botanical_gardens', 'golf', 'wholesalers', 'walking_tours', 'bike_tours', 'street_vendors', 'outlet_stores', 'hawaiian', 'ethiopian', 'pubs', 'argentine', 'vitamins_&_supplements', 'greek', 'kebab', 'tiki_bars', 'skate_shops']
labels, unique_labels = pd.factorize(all_sub)

new_sub = []
for sub_types_list in df['sub_types']:
    for i in range(len(sub_types_list)):
        sub_types_list[i] = np.where(unique_labels == sub_types_list[i])[0][0]
print(df[['main_type', 'sub_types']])