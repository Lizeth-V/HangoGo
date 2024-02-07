import re
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
dbname = "Hango"
collection_name = "User Data"

# Establish a connection to MongoDB Atlas
client = MongoClient(connection_string)

# Accessing the database
db = client[dbname]

# Accessing the collection
collection = db[collection_name]

