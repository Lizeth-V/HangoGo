import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson import ObjectId
from selenium import webdriver
import time
from concurrent.futures import ThreadPoolExecutor
#IN THEORY THIS WILL ONLY NEED TO BE RAN ONCE, MAYBE MORE IF NEW DOCUMENTS ARE ADDED AND ITS NECESSARY

#mongo info
connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"
collection_name = "Places"

#connect to the collection for hango
client = MongoClient(connection_string)
db = client[dbname]
collection = db[collection_name]

#scraping for google places imaes
def scrape_images(doc):
        #the doc should have a weblink so we can go to the page and get the image
        weblink = doc["weblink"]
        
        #run a selenium chrome browser to open the page, because it wasnt working with just bs4
        driver = webdriver.Chrome()

        driver.get(weblink)

        time.sleep(1)
        page_source = driver.page_source
        #get source and bs4 it

        soup = BeautifulSoup(page_source, 'html.parser')

        #the specific button class holds the most relevant (in google places' mind) image
        button_tag = soup.find('button', class_='aoRNLd kn2E5e NMjTrf lvtCsd')

        driver.quit()

        #if the button exits scrape the image embedded and insert it into the db documents
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

            else: print("No Visible Picture")

def multithread_scrape():
    #find all documents with weblink and not already operated on 
    l = list(collection.find({"weblink": {"$exists": True}, "image_url": {"$exists": False}}))

    #mulithread the process since we it takes so long to run one
    num_threads = 4
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(scrape_images, l)

def multithread_scrape_yelp():
    #find all yelp or google docs with no weblinks and multithread scraping it from a simple google search
    l = list(collection.find({"image_url": {"$exists": False}}))
    num_threads = 4
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(scrape_images_yelp, l)


def scrape_images_yelp(doc):
        #this prefix conducts a search for images related to following prompts
        #name and address should give us accurate results, if issues are found manually handle them
        weblink = 'https://www.google.com/search?tbm=isch&q=' + doc['name'] + doc['address']
        
        driver = webdriver.Chrome()

        driver.get(weblink)

        time.sleep(1)
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')


        #this class is repeatedly the class for images page's first image div
        div_tag = soup.find('div', class_='fR600b islir')

        driver.quit()

        if div_tag:
            img_tag = div_tag.find('img')
            image_url = img_tag.get('src')


            #upload new image link to the document
            if image_url:
                collection.update_one(
                    {"_id": doc["_id"]},
                    {"$set": {"image_url": image_url}},
                    upsert=True
                )

            else: print("No Visible Picture")

#uncomment the following to scrape 
#multithread_scrape() #for documents with google weblinks
#multithread_scrape_yelp() #for all other documents (yelp, etc.)
client.close()
