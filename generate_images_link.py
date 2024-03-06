import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson import ObjectId
from selenium import webdriver
import time


# MongoDB connection details
connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"
collection_name = "Places"

# Connect to MongoDB
client = MongoClient(connection_string)
db = client[dbname]
collection = db[collection_name]

# Function to scrape the first picture for each place with a weblink
def scrape_images():
    # Iterate through documents in the collection
    for document in list(collection.find({"weblink": {"$exists": True}})):
        weblink = document["weblink"]
        
       # Assuming you have the ChromeDriver executable in your PATH
        driver = webdriver.Chrome()

        # Replace 'your_weblink' with the actual weblink
        driver.get(weblink)

        # Get the page source after waiting for a few seconds (adjust the sleep time as needed)
        time.sleep(5)
        page_source = driver.page_source

        # Parse the HTML content
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the first button tag with the specified class
        button_tag = soup.find('button', class_='aoRNLd kn2E5e NMjTrf lvtCsd')

        print(button_tag)

        # Close the Selenium driver
        driver.quit()

        if button_tag:
            img_tag = button_tag.find('img')
            image_url = img_tag.get('src')

            # Print or save the image URL as needed
            print(f"Place: {document['name']}, Image URL: {image_url}")

            # Update the document with the image URL
            collection.update_one(
                {"_id": document["_id"]},
                {"$set": {"image_url": image_url}},
                upsert=True
            )

                #print(image_url)

# Run the scraping function
scrape_images()

# Close the MongoDB connection
client.close()
