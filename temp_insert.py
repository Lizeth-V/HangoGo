import pymongo
from pymongo import MongoClient

connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"
collection_name = "User Data"

# Establish a connection to MongoDB Atlas
client = MongoClient(connection_string)

# Accessing the database
db = client[dbname]

# Accessing the collection
collection = db[collection_name]

uname = input("Enter username =")
full_name = input("Enter fullname seperated by a space =")
email = input("Enter email=")
age = int(input("Enter age ="))
street = input("Enter street address=")
city= input("Enter city=")
state= input("Enter state abbrv.=")
zip_code= input("Enter zip code =")
country = input("Enter country abbrv. =")



# Inserting data into the collection
data_to_insert = {
    "username": uname,
    "full_name": full_name,
    "email": email,
    "age": age,
    "address": {
        "street": street,
        "city": city,
        "state": state,
        "zip_code": zip_code,
        "country": country
    }
}

insert_result = collection.insert_one(data_to_insert)
print(f"Inserted ID: {insert_result.inserted_id}")

# Reading data from the collection
query = {"full_name": full_name}  # Define a query to retrieve specific data
result = collection.find_one(query)

if result:
  print("Data found:")
  print(result)
else:
  print("No matching data found")
