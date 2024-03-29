# app.py
from bson import ObjectId
import json

import bcrypt
import os
import random
import string
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import datetime, timedelta

from flask_pymongo import PyMongo
from register import register_user, hash_password
from db import users_collection, places_collection

app = Flask(__name__)

# Lizeth - COnfigureing Flask Mail
load_dotenv()
#this is a SMTP Server used for gmail - This connects to the server and sends out the verification email 
app.config['MAIL_SERVER']= os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
# Verify
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
# Default
app.config['DEFAULT_USERNAME'] = os.getenv('DEFAULT_USERNAME')
app.config['DEFAULT_PASSWORD'] = os.getenv('DEFAULT_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# secret key (Lizeth)
app.secret_key = "supersecrethangogo!!!!"

# Calculate age (Gloria)
def calculate_age(birth_year, birth_month, birth_day):
    today = datetime.today()
    age = today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))
    return age


# Gloria
@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    print("User verified...now in create account page")
    user_id = session.get("_id")

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        birth_month = int(request.form.get("birth_month"))
        birth_day = int(request.form.get("birth_day"))
        birth_year = int(request.form.get("birth_year"))

        # Check if the user is at least 13 years old
        age = calculate_age(birth_year, birth_month, birth_day)
        if age < 13:
            return render_template("create_account.html", 
                                   error="sorry! we would love to be friends but you don’t meet our age requirements! (we don’t want to get sued pls)")
        else:
            # Update user information in the database
            users_collection.update_one({"_id": ObjectId(user_id)}, 
                                        {"$set": 
                                            {  
                                                "first_name": first_name,
                                                "last_name": last_name,
                                                "birth_month": birth_month,
                                                "birth_day": birth_day,
                                                "birth_year": birth_year,
                                                "age": age
                                            }
                                        })
            print("Form Data:", request.form) 
            print("Updated create account page", first_name, last_name, birth_month, birth_day, birth_year)
            return redirect(url_for("index"))
    else:
        return render_template("create_account.html")

# Register new User (Gloria & Lizeth)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        #email verification token generated (Lizeth)
        verification_token = ''.join(random.choices(string.ascii_letters + string.digits, k=30))

        registration_error = register_user(username, email, password, confirm_password, users_collection, verification_token)

        if registration_error is not None:
            print("Registration successful. Goes to email-verify. then create-account")
            # sending email verifcation 
            print("Send_Verification inputs: ", email," ", username," ",verification_token)
            send_verification(email, username, verification_token)
            # print(username, user)
            return render_template("verify.html")

        

        print("Registration error:", registration_error)
        # comment out below the one line of code below before presentation and launch
        print("Form values:", username, email, password, confirm_password)
        return render_template("register.html", error=registration_error)
        

    return render_template("register.html")

# Gloria
@app.route("/login", methods= ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = users_collection.find_one({"username": username})

        if user:
            # Get the hashed password from the user object
            hashed_password = user["password"]

            # Assuming `hashed_password` is currently a string
            # Convert it to bytes using `encode()`
            hashed_password_bytes = hashed_password.encode("utf-8")

            # check if the password the user entered matches the hashed password
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password_bytes):
                # password is matched
                # convert ObjectId to string for JSON serialization
                user["_id"] = str(user["_id"])
                session["user"] = user
                print("Login Success")
                return redirect(url_for("landing_page", username=username))
            else:
                # password did not match
                print("Invalid username or password")

        else:
            # User not found
            print("User not found.")
    return render_template("login.html")


# Landing Page that will display the chatbox and the user profile  - (Gloria & Lizeth)
# Also allows users to update thier name and email if preferred - but won't reverify emails
@app.route('/<username>', methods=['GET', 'POST'])
def landing_page(username):
    user = session.get('user')
    
    if not user:
        return redirect(url_for('login'))
    
    # Retrive user session information
    user_id = user.get('_id')
    username = user['username']
    # Retrieve user information from the database
    user_from_db = users_collection.find_one({"_id": user_id})
    
    # This should update the users changes in the Editing mode in their profile (Lizeth)
    if request.method == 'POST':
    # get the new user data from the form  
        print("User updating info")
        first_name = request.form.get('edit_first_name')
        last_name = request.form.get('edit_last_name')
        email = request.form.get('edit_email')

        # update the database
        # making a dictionary with the fields that are not None (left empty)
        update_data = {}
        if first_name:
            update_data['first_name'] = first_name
        if last_name:
            update_data['last_name'] = last_name
        if email:
            update_data['email'] = email

        # updating database with the new changes (ignoring empty fileds)
        if update_data:
            users_collection.update_one(
                {'username': username},
                {'$set': update_data}
            )
            print("update user successful..?")
        else:
            print("no changes made")

        return redirect(url_for('landing_page', username=username))
    

    return render_template("landing_page.html",
                           user=user_from_db,
                           username = username,
                           first_name = user["first_name"],
                           last_name = user["last_name"],
                           email = user["email"],
                           birth_month = user["birth_month"],
                           birth_day = user["birth_day"],
                           birth_year = user["birth_year"]
                           )  

# Gloria
# Add to Favorites List

# temp sample data for list of places, temp placeholder for AI generated suggested places
# place_list = [
#     {"name": "Place 1", "address": "Address 1"},
#     {"name": "Place 2", "address": "Address 2"},
#     {"name": "Place 3", "address": "Address 3"}
# ]
# saved_places = []
# test share locations with the places weblinks

query = {"sub_types": "cafe"}
place_list = places_collection.find(query)
saved_places =[]


# Gloria
@app.route('/add_to_favorites', methods = ["POST"])
def add_to_favorites():
    place_index = int(request.form['place_index'])
    place = place_list[place_index]
    if place in saved_places:
        return jsonify(success=False, message=" ")
    else:
        saved_places.append(place)
        print(saved_places)
        return jsonify(success=True, message = "Added to Favorites List")
# Gloria
@app.route("/")
def index():
    return render_template("index.html")

# Sending Email Verifications (Lizeth)
@app.route("/verify/<username>/<token>")
def verify(username, token):
    # After the user register their account with an email or password they get redirected to this verify page that indiactes them to check their email to verify their account 
    print("verify page")
    user = users_collection.find_one({'username': username,'verification_token': token, 'token_expiration': {'$gt': datetime.utcnow()}})
    # Only if user has already registered
    if user:
        # Mark user as verified in the database
        users_collection.update_one({'_id': user['_id']}, {'$set': {'verified': True}})

        flash('Email verification successful! You can now log in.')
        print("Email Verified...Redirect to create Account")
        return redirect(url_for("create_account"))

    flash('Invalid or expired verification link.')
    return redirect(url_for("verify", username=username))

# Function to organize sending emails through default or verify 
def get_sender(choice, app):
    if choice == 1:
        # choice 1 - verify email 
        return app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']
    else:
        # choice 2 - default email
        return app.config['DEFAULT_USERNAME'], app.config['DEFAULT_PASSWORD']

# Lizeth
def send_verification(email, username, token):
    # Sends Verification Email from the Hangogo Verification email. The email contains unique link to verify a users account. 
    # sender, sender_psw = 
    get_sender(1, app) #'1' to send email from the verify email 
    msg = Message('Verify Your Email - Hangogo', sender = 'hangogo.verify@gmail.com' ,recipients=[email])
    verification_link = url_for('verify', username=username,token=token, _external=True)
    msg.body = f'Hi! I cant wait to be friends! Click the following link to verify your email: {verification_link}'

    try:
        mail.send(msg)
        print("Email Sent!")
    except Exception as e:
        flash(f"Failed to send email. Error: {str(e)}")

    return "Verification email sent"


# Map Page (Lizeth)
@app.route("/map")
def map():
    # Retrive user session information
    user = session.get('user')

    if user is None:
        flash('Please log in to access the map.')
        return redirect(url_for('login'))
    
    # Retrieve user information from the database
    # user_id = user.get('_id') 
    # user_from_db = users_collection.find_one({"_id": user_id})
    print("Redirected to Map Page!")
    return render_template('map.html', user=user)

# About Us/ How to use the site (Lizeth)
@app.route("/about_us")
def about_us():
    print("Redirect to About Us page!")
    return render_template('about_us.html')

# Delete Account (Lizeth)
@app.route("/delete_account", methods=["POST"])
def delete_acct():
    print("Delete Account")

    user = session.get('user')
    user_id = user.get('_id')

    try:
        result = users_collection.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count == 1:
            # Account deletion successful, redirect to the index page or any other desired destination
            # Clear user session
            print('Delete Account Success')
            session.pop('user', None)
            return redirect(url_for('index'))
        else:
            flash('Failed to delete account.')
    except Exception as e:
        flash('Failed to delete account.')

    return redirect(url_for('index'))

@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():

    if request.method == "POST":
        email = request.form.get("email")
        user_inDB = users_collection.find_one({'email': email})

        if user_inDB:
            print("Valid User in DB - generating token")
            reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
            reset_email(email, reset_token)
            print("reset psw email sent!")
            return render_template('recovery.html')

        else:
            print("Email not valid")
            flash('Email not valid')

    return render_template("forgot_password.html")
            
    

@app.route("/reset_sent")
def reset_sent():
    return render_template('recovery.html')

def reset_email(email, token):
    # Sends Reset Password Email from the official Hangogo email. The email contains unique link to users so they can securely recovery their  account. 
    get_sender(2, app) #'2' to send email from the default email 
    msg = Message('Verify Your Email - Hangogo', sender = 'letshangogo@gmail.com' ,recipients=[email])
    reset_link = url_for('reset_password', token=token, _external = True)
    msg.body = f'Hi! Trouble signing in? No worries just click the following link to reset your password ->  {reset_link}'

    try:
        mail.send(msg)
        print("Email Sent!")
    except Exception as e:
        flash(f"Failed to send email. Error: {str(e)}")

    return "Reset Password email sent"

@app.route("/reset_password/<token>")
def reset_password(token):
    return render_template("reset_password.html")

# Gloria
# send contact form
def send_contact_form(result):
    sender = 'letshangogo@gmail.com'
    recipients = [result["email"], sender]
    subject = "Feedback from {}".format(result["email"])
    msg = Message(subject, sender = sender, recipients=recipients)

    msg.body = """
    Hello There,

    The feedback you left us:
    Email: {}
    Message: {}

    -hangogo Webmaster
    """.format(result["email"], result["message"])


    mail.send(msg)
    print("Contact form sent")

# Gloria
# contact us/report an issue form
@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        try:
            result = {}
            result["email"] = request.form.get("email").replace(' ', '').lower()
            result["message"] = request.form.get("message")

            send_contact_form(result)
            print("email sent")
            return redirect(url_for("index"))
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template("contact.html")



# Gloria
# favorites page
@app.route("/favorites")
def favorites():
    user = session.get("user")
    if user is None:
        flash("Please log in to access favorites page.")
        return redirect(url_for("login"))
    
    page = request.args.get("page", default=1, type=int)
    per_page = 10
    query = {"sub_types": "cafe"}
    places = places_collection.find(query)
    total_places = 24 #hard code the total places count() does not work
    places = places.skip((page - 1) * per_page).limit(per_page)
    favorites_list = []
    for place in places:
        favorites_list.append({
            "icon": place["image_url"],
            "name": place["name"],
            "address": place["address"]
        })
    return render_template("favorites.html", favorites=favorites_list, page=page, per_page=per_page, total_places=total_places)

# Gloria
# get place from DB
@app.route('/get_place', methods=['POST'])
def get_place():
    # Retrieve the selected place from MongoDB
    place_id = request.form['place_id']
    place = places_collection.find_one({"_id": ObjectId(place_id)})
    return jsonify(place)


if __name__ == "__main__":
    app.run(debug=True)