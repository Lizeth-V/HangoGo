# register.py

import re
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session
# from pymongo import MongoClient
from db import users_collection

app = Flask(__name__)


def hash_password(password):
    try:
        # Check if password is a string
        if not isinstance(password, str):
            return "Password must be a string"
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed_password
    except Exception as e:
        print("Error hashing password:", e)
        return None


def is_email_valid(email):
    # Regular expression for a simple email validation
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(email_regex, email)

def register_user(username, email, password, confirm_password):

    # Check if email is valid
    if not is_email_valid(email):
        return "Invalid email address"
    
        # # Check if password is provided
    if password is None:
        return "Password is required"
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
        "email": email,
        "password": hashed_password

    }
    result = users_collection.insert_one(user_data)

    # Store the user's _id in the session
    # Convert ObjectId to string for session storage
    session["_id"] = str(result.inserted_id)  
    return render_template("create_account.html")
