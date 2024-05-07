# app.py
from bson import ObjectId
import json

import bcrypt
import os
import random
import string
import googlemaps

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, g
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import datetime, timedelta

from flask_pymongo import PyMongo
from register import register_user, hash_password
from db import users_collection, places_collection
from reset import reset_psw

import temp_feedback
import return_highest_rec as retH
import generate_model
from bson import ObjectId
import math
import get_history

from pymongo import MongoClient
import initial_recommend as retI

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

# Get Google Maps API key from environment variable
# google_maps_api_key = str(os.getenv('GOOGLE_MAPS_API'))
google_maps_api_key = "AIzaSyDC1Ysg0I0IHqCs_TDxFwkMJDK71zruEGk"

# Initialize Google Maps API client with API key
gmaps = googlemaps.Client(key=google_maps_api_key)

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
            #  Store user_id in session
            session["user_id"] = str(user_id)
            print("Redirecting to interest_form page")
            return redirect(url_for("interest_form"))
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

# Initial interests quiz results (Lizeth)
@app.route("/interest_form", methods=["GET", "POST"])
def interest_form():
    print("Completed create account.. now in interest form!")
    user_id = session.get("user_id")

    if not user_id:
        return "User not authenticated. Please create an account first."

    user_data = users_collection.find_one({"_id": ObjectId(user_id)})

    if not user_data:
        return "User data not found. Please try again."

    if request.method == 'POST':
        interest_arr = request.form.getlist('selections')
        # Update user's interests in the database
        users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"interests": interest_arr}})
        
        print("Submitted initial interest form successfully!")
        return render_template("hello.html", next=url_for('index'))
        # return redirect(url_for("landing_page", username=user_data["username"]))
    
    return render_template("interests.html")


# Gloria
@app.route("/login", methods= ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = users_collection.find_one({"username": username}, {"_id": 1, "password": 1, "username": 1})

        if user:
            # Get the hashed password from the user object
            hashed_password = user["password"]

            # Assuming hashed_password is currently a string
            # Convert it to bytes using encode()
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


# Logout and clear the user session (Lizeth)
@app.route("/logout")
def logout():
    # session.pop('username', None)
    session.clear()
    print("Logout Success")
    return render_template("byebye.html", next=url_for('index'))


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
    user_id = user.get('_id')
    username = user['username']

    user_from_db = users_collection.find_one({"_id": ObjectId(user_id)},{"_id": 1, "username": 1, "first_name": 1, "last_name": 1, "email": 1, 
     "birth_month": 1, "birth_day": 1, "birth_year": 1})

    print(user_from_db)
    
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
            users_collection.update_one({'username': username},
                        {'$set': update_data})
            print("update user successful..?")
        else:
            print("no changes made")

        return redirect(url_for('landing_page', username=username))


    return render_template("landing_page.html",
                                user=user_from_db,
                                user_id = user_id,
                                username = username,
                                first_name = user_from_db["first_name"],
                                last_name = user_from_db["last_name"],
                                email = user_from_db["email"],
                                birth_month = user_from_db["birth_month"],
                                birth_day = user_from_db["birth_day"],
                                birth_year = user_from_db["birth_year"]
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
# add place to favorites
@app.route('/add_to_favorites', methods=["GET"])
def add_to_favorites():
    user_id = session.get("_id")
    place_index = request.form.get("place_index")

    if not place_index.isdigit():
        return jsonify(success=False, message="Invalid place index")

    index = int(place_index)
    if index < 0 or index >= len(place_list):
        return jsonify(success=False, message="Invalid place index")

    place_id = str(place_list[index]["_id"])  # Convert _id to string

    result = users_collection.find_one({'_id': ObjectId(user_id)})

    favorite_list = result.get('favorite_list', [])

    for place in favorite_list:
        if place == place_id:
            return jsonify(success=False, message="Already in Favorites List")

    users_collection.update_one({'_id': ObjectId(user_id)}, {'$addToSet': {'favorite_list': place_id}})

    temp_feedback.add_to_favorites_update(user_id=user_id, place_id=place_id)
    connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
    client = MongoClient(connection_string)
    db = client["Hango"]
    collection_name = "ratings"
    collection = db[collection_name]
    query = {"user_id": user_id}

    count = collection.count_documents(query)
    client.close()

    # Nhu's additional code starts here
    # Assuming g.db_count is intended to hold the count of places rated by the user
    places_in_db = count

    if places_in_db >=9:
        generate_model.generate_place_probabilities(user_id)

    return jsonify(success=True, message="Added to Favorites List")

#Gloria
# remove place from favorites
@app.route('/remove_from_favorites', methods =["POST"])
def remove_from_favorites():
    user_id = session.get("_id")
    place_id = request.form["place_id"]
    users_collection.update_one({'_id': ObjectId(user_id)}, {'$pull': {'favorite_list': str(place_id)}})
    return jsonify(success=True, message="Removed from Favorites List")

# Gloria
@app.route("/")
def index():
    if 'user' in session:
        user = session['user']
        username = user.get('username') 
        return render_template('index.html', username=username)
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
    return redirect(url_for("verify", username=username, token=token))

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
    ''' #this will update the map to the place reccomended in chatbox and is to be connected when chatbox is on page...

    # Retrieve place information based on user's session
    place_name = user.get('place_name')  # Assuming place_name is stored in the user session
    place_info = get_place_info(place_name)
    
    # Check if place information is available
    if place_info:
        return render_template('map.html', user=user, place_info=place_info)
    else:
        flash('Place information not found.')
        return redirect(url_for('map.html'))  # Redirect to map page with error?
    '''

# About Us/ How to use the site (Lizeth)
@app.route("/about_us")
def about_us():
    print("Redirect to About Us page!")
    username = session.get('user')  # Retrieve username from session
    if username:
        return render_template('about_us.html', username=username)
    else:
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

# Forget Password (Lizeth)
@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():

    if request.method == "POST":
        email = request.form.get("email")
        user_inDB = users_collection.find_one({'email': email})

        if user_inDB:
            print("Valid User in DB - generating token")
            # making a reset_token and adding it on to the user information 
            reset_token = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
            users_collection.update_one({'email': email}, {"$set": {"reset_token": reset_token}})
            reset_email(email, reset_token)
            print("reset psw email sent!")
            return render_template('recovery.html')

        else:
            print("Email not valid")
            flash('Email not valid')

    return render_template("forgot_password.html")
            
    
# Sending an email to reset password (Lizeth)
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

# Unique link that will reset the usesrs password and send them back to login after successfully changing password
@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):

    if request.method == "POST":
        newPassword = request.form.get("new_psw")
        newConfirm_password = request.form.get("reenter_psw")

        if newPassword != newConfirm_password:
            flash("Passwords do not match. Try Again")
            return render_template("reset_password.html", token=token)
        
        # find user with the reset token
        user = users_collection.find_one({"reset_token": token})
        if user:
            reset_psw(user["username"], newPassword, users_collection)
            flash("Password has be reset successfully! You can now Login")

            # clearing the user reset token after being used.
            users_collection.update_one({"_id": user["_id"]}, {"$unset": {"reset_token": ""}})

            # Render the loading page before redirecting to the login page
            return render_template("loading.html", next=url_for('login'))

        else:
            flash("Invalid or expired token.")
            return render_template("reset_password.html", token=token)

    return render_template("reset_password.html", token=token)

# Users can change their passwords from their account page (Lizeth)
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    print("In Change Password Page")
    # Retrive user session information
    user = session.get('user')
    print(user)
    
    if user is None:
        # redirect to login if user is not signed in
        return redirect(url_for('login'))
    
    if request.method == "POST":
        newPassword = request.form.get("new_psw")
        newConfirm_password = request.form.get("reenter_psw")
        current_password = request.form.get("old_psw")

        if newPassword != newConfirm_password:
            flash("Passwords do not match. Try Again")
            return render_template("change_password.html")
        
        username = user.get('username')
        # Verify current password in order to reset password
        if not verify_password(username, current_password):
            print("Incorrect Current Password.")
            return render_template("change_password.html")
        
        # Reseting the password
        reset_psw(user["username"], newPassword, users_collection)
        print("password reset!")
        flash("Password has be reset successfully! You can now Login")
        return redirect(url_for("login"))
        

    return render_template("change_password.html")

def verify_password(username, current_password):
    # Retrieve the user's information
    user = users_collection.find_one({'username': username})
    print(user)

    if user:
        # Retrieve the hashed password from the database
        hashed_password = user.get('password')

        if hashed_password is not None:
            # Check password matches the hashed password
            if bcrypt.checkpw(current_password.encode("utf-8"), hashed_password.encode("utf-8")):
                return True
            else:
                return False
        else:
            print("Error: Hashed password is NONE")
            return False
    else:
        # User not found
        return False

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

@app.route('/add_to_favorites2', methods = ["GET"])
def add_to_favorites2():
    import favorite

    user = session.get('user')
    user_id = user.get('_id')

    place_id = request.args.get('place_id', default='5', type=str)
    
    favorite.add_to_favorites(user_id, place_id)
    temp_feedback.add_to_favorites_update(user_id=user_id, place_id=place_id)

    connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
    client = MongoClient(connection_string)
    db = client["Hango"]
    collection_name = "ratings"
    collection = db[collection_name]
    query = {"user_id": user_id}

    count = collection.count_documents(query)
    client.close()

    # Nhu's additional code starts here
    # Assuming g.db_count is intended to hold the count of places rated by the user
    places_in_db = count

    if places_in_db < 10:
        generate_model.generate_place_probabilities(user_id)


    return jsonify(success=True, message = "Added to Favorites List")

# Gloria
# favorites page
@app.route("/favorites", methods=["GET"])
def favorites():
    # Retrive user session information
    user = session.get('user')

    if user is None:
        flash("Please log in to access favorites page.")
        return redirect(url_for("login"))

    user_id = user["_id"]

    query = {"_id" : ObjectId(user_id)}

    user_profile = users_collection.find_one(query)
    
    if user_profile:
        favorite_list = user_profile.get('favorite_list', [])
        total_places = len(favorite_list)

        page = request.args.get("page", default=1, type=int)
        per_page = 2
        start_index = (page - 1) * per_page
        end_index = min(start_index + per_page, total_places)
        paginated_favorites = favorite_list[start_index:end_index]

        favorites_info = []
        for place_id in paginated_favorites:
            place_query = {"_id": ObjectId(place_id)}
            place_info = places_collection.find_one(place_query)
            if place_info:
                favorites_info.append({
                    "icon": place_info.get("image_url", ""),
                    "name": place_info.get("name", ""),
                    "address": place_info.get("address", "")
                })

        return jsonify({
            "favorites": favorites_info,
            "page": page,
            "per_page": per_page,
            "total_places": total_places
        })
    else:
        flash("User not found.")
        return redirect(url_for("login"))



# Gloria
# get place from DB
@app.route('/get_place', methods=['POST'])
def get_place():

    # Retrieve the selected place from MongoDB
    place_id = request.form['place_id']
    place = places_collection.find_one({"_id": ObjectId(place_id)})
    return jsonify(place)

# This page will display the top locations people like and are visiting (Lizeth)
@app.route("/top_locations")
def top_locations():
    username = session.get('user')  # Retrieve username from session

    # Fetch top 10 places with the best ratings from DB
    # TO-DO: add location recognition - so users can see top places in their area 
    top_places = places_collection.find().sort('rating', -1).limit(10)

    if username:
        return render_template('top_locations.html', username=username, top_places=top_places)
    else:
        return render_template('top_locations.html', top_places=top_places)
    
# Collections Page (Lizeth) - this is a page that includes curated places based on a specific theme
@app.route("/collections")
def collections():
    username = session.get('user')
    if username:
        return render_template('collections.html', username=username)
    else:
        return render_template('collections.html')

@app.route("/cafe_culture")
def cafe_culture():
    username = session.get('user')
    # temp for testing:
    top_placesC = places_collection.find({"main_type": "Drinks"}).sort('rating', -1).limit(10)
    top_places = list(top_placesC)

    place_data = []

    for p in top_places:
        coordinates = {'lat': p['lat'], 'lng': p['lon']}
        place_data.append({'name': p['name'], 'coordinates': coordinates})

    # place_coordinates = []

    # for p in top_places:
    #     coordinates = {'lat': p['lat'], 'lng': p['lon']}
    #     place_coordinates.append(coordinates)
    # print("Coordinates:", place_coordinates)


    if username:
        return render_template('cafe_culture.html', username=username, top_places=top_places, place_data=place_data)
        # return render_template('cafe_culture.html', username=username, top_places=top_places, place_coordinates=place_coordinates)
        # return render_template('cafe_culture.html', username=username, packed=zip(top_places, place_coordinates))
    else:
        return render_template('cafe_culture.html',top_places=top_places, place_data=place_data)
        # return render_template('cafe_culture.html',top_places=top_places, place_coordinates=place_coordinates)
        # return render_template('cafe_culture.html', packed=zip(top_places, place_coordinates))

# Gloria
#itinerary planner GET
@app.route('/itinerary_planner', methods=["GET"])
def choose_places_to_go():
    return render_template("itinerary_planner.html")

# Gloria
# itinerary planner POST
@app.route('/plan_trip', methods=['POST'])
def plan_trip():
    selected_places = request.form.getlist('places')
    travel_mode = request.form['travelMode']
    coordinates = []

    # Fetch coordinates for selected places from MongoDB
    for place_name in selected_places:
        place = places_collection.find_one({'name': place_name})
        if place and 'address' in place:
            # Use the address from MongoDB to obtain coordinates from Google Maps Geocoding API
            geocode_result = gmaps.geocode(place['address'])
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                coordinates.append({'lat': location['lat'], 'lng': location['lng']})

    # Request directions using Google Maps Directions API
    directions = []
    for i in range(len(coordinates) - 1):
        start_coord = coordinates[i]
        end_coord = coordinates[i + 1]
        direction = gmaps.directions(
            (start_coord['lat'], start_coord['lng']),
            (end_coord['lat'], end_coord['lng']),
            mode=travel_mode
        )
        directions.append(direction)

    # Pass directions and other data to the output page
    return render_template('trip_summary.html', directions=directions)


# Gloria
# multi recommendation page to allow user to add other user and use the location based

#Gloria
#add another user for multi rec


# User_data temp placement, remove before deployment
user_data = {
    "user1": {"name": "User 1", "location": "Glendale"},
    "user2": {"name": "User 2", "location": "Los Angeles"},
    # Add more users here...
}

@app.route('/add_another_user_for_rec', methods=['GET','POST'])
def add_another_user_for_rec():
    if request.method == "POST":
        user_id = request.form.get('user_id')
        user_name = request.form.get('user_name')
        user_location = request.form.get('user_location')
        user_data[user_id] = {"name": user_name, "location": user_location}
        return jsonify({"message": "User added successfully"})
    return render_template("add_another_user_for_rec.html", user_data=user_data)


import multi_rec as multiR
# Gloria
# generate recommendation for multiple users placeholder, Nhu will have the alogorithm how it generates the places from the 2 locations
@app.route('/multi_recommendation', methods=['POST'])
def multi_recommendation():
    user = session.get('user')
    user_id = user.get('_id')
    target_user_id = request.json.get('target_user_id')
    target_location = user_data.get(target_user_id, {}).get('location')
    # Logic to generate recommendations based on target_location
    
    #take inspiration from aidan's new_active_place code (now for multiple users)
    #user_id in an array
    #target_location (one of locations, center of location, or new location)
    multiR.get_multi_rec(user_id, target_location)
    recommendations = ["user1", "user2"]  # Dummy recommendations
    return jsonify({"recommendations": recommendations})


'''# Nhu
# check database and update app with database changes
def check_database():
    user = session.get('user')
    user_id = user["_id"]
    connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
    client = MongoClient(connection_string)
    db = client["Hango"]
    collection_name = "ratings"
    collection = db[collection_name]
    query = {"user_id": user_id}
    g.db_count = collection.count_documents(query)'''


@app.route('/get_db_data')
def get_data():
    user = session.get('user')
    user_id = user["_id"]

    connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
    client = MongoClient(connection_string)
    db = client["Hango"]
    collection_name = "ratings"
    collection = db[collection_name]
    query = {"user_id": user_id}

    count = collection.count_documents(query)
    client.close()

    # Nhu's additional code starts here
    # Assuming g.db_count is intended to hold the count of places rated by the user
    places_in_db = count

    data = {
        'db_count': places_in_db
        }
    return jsonify(data)


#Nhu
#get coordinates for input location
@app.route('/get_coordinates', methods=['GET', 'POST'])
def get_coord_data():
    connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
    client = MongoClient(connection_string)
    db = client["Hango"]
    city = request.args.get('city', default=None, type=str)
    query = {"Name": city}
    coordinates = {
        "Coordinates": db["Location"].find_one(query)['Coordinates']
    }
    client.close()

    return jsonify(coordinates)

#(Aidan)
#take in the parameters and return a recommendation, from the AI
@app.route('/get_new_active_place', methods=['GET', 'POST'])
def get_active_place_details():
    user = session.get('user')
    user_id = str(user.get('_id'))
    radius = request.args.get('radius', default=5, type=int)
    place_type = request.args.get('place_type', default=None, type=str)
    lat = request.args.get('lat', default=None, type=float)
    long = request.args.get('long', default=None, type=float)

    connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
    client = MongoClient(connection_string)
    db = client["Hango"]
    collection_name = "ratings"
    collection = db[collection_name]
    query = {"user_id": user_id}

    count = collection.count_documents(query)
    client.close()

    # Nhu's additional code starts here
    # Assuming g.db_count is intended to hold the count of places rated by the user
    places_in_db = count

    if places_in_db < 10:
        active_place = retI.get_one_initial_recommend(user_id, lat=lat, long=long)
    #end
    else:
        active_place = retH.match_highest_list(
        retH.get_highest_list(user_id),
        lat=lat,
        long=long,
        radius=radius,
        place_type=place_type
        )
    #Convert all ObjectId instances to strings for easier coding
    active_place = convert_objectid(active_place)

    #Return data to be displayed and used, as json.
    return jsonify({'active_place': active_place})

#(Aidan)
#convert to string for handling bson objects
def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectid(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None  
    else:
        return obj

#(Aidan)
#Called when user presses accept
@app.route('/accept_rec/', methods=['GET'])
def accept_rec_model():
    #takes user and place parameters and inputs the feedback and regenerates the model for the user
    user = session.get('user')
    user_id = str(user.get('_id'))
    place_id = request.args.get('place_id', default=None, type=str)
    temp_feedback.accept_recommendation_update(user_id=user_id, place_id=place_id) #update the feedback page

    connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
    client = MongoClient(connection_string)
    db = client["Hango"]
    collection_name = "ratings"
    collection = db[collection_name]
    query = {"user_id": user_id}

    count = collection.count_documents(query)
    client.close()


    # Nhu's additional code starts here
    # Assuming g.db_count is intended to hold the count of places rated by the user
    places_in_db = count

    if places_in_db >=9:
        generate_model.generate_place_probabilities(user_id)

    return 'Success' 

#(Aidan)
#Called when user presses decline
@app.route('/decline_rec/', methods=['GET'])
def decline_rec_model():
    #takes user and place parameters and inputs the feedback and regenerates the model for the user
    user = session.get('user')
    user_id = str(user.get('_id'))
    place_id = request.args.get('place_id', default=None, type=str)


    temp_feedback.decline_recommendation_update(user_id=user_id, place_id=place_id)

    connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
    client = MongoClient(connection_string)
    db = client["Hango"]
    collection_name = "ratings"
    collection = db[collection_name]
    query = {"user_id": user_id}

    count = collection.count_documents(query)

    client.close()


    # Nhu's additional code starts here
    # Assuming g.db_count is intended to hold the count of places rated by the user
    places_in_db = count

    if places_in_db >=9:
        generate_model.generate_place_probabilities(str(user_id))

    return 'Success'


#(Aidan)
#Called when user presses block
@app.route('/block_rec/', methods=['GET'])
def block_rec_model():
    #takes user and place parameters and inputs the feedback and regenerates the model for the user, prevents this place from being shown again.
    user = session.get('user')
    user_id = str(user.get('_id'))
    place_id = request.args.get('place_id', default=None, type=str)

    temp_feedback.block_recommendation_update(user_id=user_id, place_id=place_id)

    connection_string = "mongodb+srv://hangodb:hangodb@cluster0.phdgtft.mongodb.net/"
    client = MongoClient(connection_string)
    db = client["Hango"]
    collection_name = "ratings"
    collection = db[collection_name]
    query = {"user_id": user_id}

    count = collection.count_documents(query)

    client.close()

    # Nhu's additional code starts here
    # Assuming g.db_count is intended to hold the count of places rated by the user
    places_in_db = count

    if places_in_db >=9:
        generate_model.generate_place_probabilities(str(user_id))

    return 'Success'

#(Aidan)
@app.route('/save_chat/', methods=['GET'])
def save_messages():
    #accept user id in the url and replace
    user = session.get('user')
    user_id = str(user.get('_id'))
    #accept arguments from url
    radius = request.args.get('radius', default=None, type=int)
    place_type = request.args.get('place_type', default=None, type=str)
    place_name = request.args.get('place_name', default=None, type=str)
    user_action = request.args.get('user_action', default=None, type=str)


    #structure of the chat history storage
    user_req_message = 'You' + ' asked for a recommendation'
    if place_type:
        user_req_message = user_req_message + ' involving ' + place_type
    if radius:
        user_req_message = user_req_message + ' in a radius of ' + str(radius) +' miles'
    user_req_message = user_req_message + '.'

    temp_feedback.insert_user_chat(user_id=user_id, string=user_req_message, source='hango')

    #also store the user feedback
    if user_action == 'decline':
        rec_message = 'Hango recommended ' + place_name + ' and you ' + user_action + 'd it.'
    else:
        rec_message = 'Hango recommended ' + place_name + ' and you ' + user_action + 'ed it.'

    #save to database
    temp_feedback.insert_user_chat(user_id=user_id, string=rec_message, source='user')

    return 'Success'

#(Aidan)
#when called, it brings in the user chat history and inflates their history page with it
@app.route('/inflate_user_history', methods=['GET'])
def fetch_user_history():
    user = session.get('user')
    user_id = str(user.get('_id'))
    user_rec_history = get_history.get_user_history(user_id)
    
    #return the chat history as a json to be able to print
    return jsonify({'history': user_rec_history})

#(Aidan)
#flask call to delete user histories
@app.route('/delete_user_chats', methods=['GET'])
def delete_user_history():
    user = session.get('user')
    user_id = str(user.get('_id'))
    temp_feedback.delete_user_chat_history(user_id)
    
    return 'Success'


@app.route('/fetch_user_active_place', methods=['GET'])
def get_user_active():
    user = session.get('user')
    user_id = str(user.get('_id'))

    try:
        place_details = temp_feedback.get_active_place(user_id)
        if place_details and '_id' in place_details:
            place_details['_id'] = str(place_details['_id'])
        else:
            return jsonify({'name': None})
    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred while fetching the active place'}), 500

    return jsonify(place_details)

@app.route('/remove_user_active_place', methods=['GET'])
def remove_user_active():
    user = session.get('user')
    user_id = str(user.get('_id'))

    temp_feedback.remove_active_place(user_id)

    return 'Success'



if __name__ == '__main__':
    app.run(debug=True)
