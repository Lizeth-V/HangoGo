# register.py

import re
import bcrypt
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from db import users_collection

app = Flask(__name__)


def hash_password(password):
    # Hash the password
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def is_email_valid(email):
    # Regular expression for a simple email validation
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(email_regex, email)

def register_user(username, email, password, confirm_password):
    # Hash the password before storing it in the database
    hashed_password = hash_password(password)

    # Check if email is valid
    if not is_email_valid(email):
        return "Invalid email address"
    
    # Hash the password
    hashed_password = hash_password(password)

    # Check if email is already taken
    if users_collection.find_one({"email": email}):
        return "Email is already taken"

    # Check if passwords match
    if password != confirm_password:
        return "Passwords do not match"
    
    # Inserting user data into the collection
    user_data = {
        "username": username,
        # "full_name": full_name,
        "email": email,
        "password": hashed_password,
        # "age": age,
        # "address": {
        #     "street": street,
        #     "city": city,
        #     "state": state,
        #     "zip_code": zip_code,
        #     "country": country
        #}
    }
    users_collection.insert_one(user_data)

    return None
