# create_account.py

from flask import Flask, render_template, request, redirect, url_for
# from pymongo import MongoClient
from datetime import datetime
from db import users_collection

app = Flask(__name__)

# Calculate age
def calculate_age(birth_year, birth_month, birth_day):
    today = datetime.today()
    age = today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))
    return age

def user_create_account(first_name, last_name, birth_month, birth_day, birth_year, age):
        # Check if the user is at least 13 years old
        age = calculate_age(birth_year, birth_month, birth_day)
        if age < 13:
            return render_template("create-account.html", error = "You must be at least 13 years old")
        
        # Inserting user data into the collection
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "birth_month": birth_month,
            "birth_day": birth_day,
            "birth_year": birth_year,
            "age": age
        }
        users_collection.insert_one(user_data)
        return None
        

