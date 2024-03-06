import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson import ObjectId
from selenium import webdriver
import dda
import time
from concurrent.futures import ThreadPoolExecutor


# MongoDB connection details
connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"
collection_name = "Places"

# Connect to MongoDB
client = MongoClient(connection_string)
db = client[dbname]
collection = db[collection_name]

# Function to scrape the first picture for each place with a weblink
def scrape_images(doc):
        weblink = doc["weblink"]
        
        driver = webdriver.Chrome()

        driver.get(weblink)

        time.sleep(1)
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        button_tag = soup.find('button', class_='aoRNLd kn2E5e NMjTrf lvtCsd')

        print(button_tag)

        driver.quit()

        if button_tag:
            img_tag = button_tag.find('img')
            image_url = img_tag.get('src')

            print(f"Place: {doc['name']}, Image URL: {image_url}")

            if image_url:
                collection.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"image_url": image_url}},
                    upsert=True
                )

            else: print("No Visiible Picture")

def multithread_scrape():
    l = list(collection.find({{"weblink": {"$exists": True}, "image_url": {"$exists": False}}}))

    num_threads = 4
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(scrape_images, l)

    

multithread_scrape()
client.close()
