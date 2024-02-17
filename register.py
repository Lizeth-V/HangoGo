# register.py

import re
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session
# from pymongo import MongoClient
from db import users_collection
from datetime import datetime, timedelta


app = Flask(__name__)


def hash_password(password):
    try:
        # Check if password is a string
        if not isinstance(password, str):
            return "Password must be a string"
        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed_password.decode("utf-8")
    except Exception as e:
        print("Error hashing password:", e)
        return None


def is_email_valid(email):
    if email is None:
        return False
    # Regular expression for a simple email validation
    email_regex = r"^\S+@\S+\.\S+$"

    if re.fullmatch(email_regex, email):
        return True
    else:
        return False

def register_user(username, email, password, confirm_password,  users_collection, verification_token):

    # Check if email is valid
    if is_email_valid(email) is False:
        return "Invalid email"

    # Check if password is provided
    if not password:
        return "Password is required"
    
    # Hash the password
    hashed_password = hash_password(password)

    # Check if password hashing was successful
    if hashed_password is None:
        return "Error hashing password"

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
        "password": hashed_password,
        "verification_token": verification_token,
        "verified": False,
        'token_expiration': datetime.utcnow() + timedelta(hours=24),

    }
    result = users_collection.insert_one(user_data)

    # Store the user's _id in the session
    # Convert ObjectId to string for session storage
    session["_id"] = str(result.inserted_id)  
    return render_template("register.html")
