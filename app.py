
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

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('pwd')

        user = collection.find_one({'username': username, 'password': password})

        if user: 
            session['user'] = user
            flash('Login Successful! :)', 'success')
            # return redirect(url_for) -- redirect to main page aka where chatbox is 
        else:
            flash('Invalid username or password. Try again..')
    return render_template('login.html')