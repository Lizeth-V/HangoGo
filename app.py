# app.py
from bson import ObjectId
import json

import bcrypt
import os
import random
import string
import googlemaps
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask_pymongo import PyMongo
from register import register_user, hash_password
from db import users_collection, places_collection

app = Flask(__name__)


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


# Gloria
@app.route('/<username>.html')
def landing_page(username):
    user = users_collection.find_one({"username": username})
    if user is None:
        return "Page not found", 404
    return render_template("landing_page.html",
                           username = username,
                           first_name = user["first_name"],
                           last_name = user["last_name"],
                           email = user["email"],
                           birth_month = user["birth_month"],
                           birth_day = user["birth_day"],
                           birth_year = user["birth_year"],
                           place_list=place_list # recommended places is the temp placeholder for the AI generated suggested places
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
place_list = list(places_collection.find(query))
favorite_list =[]


# Gloria
# add place to favorites
@app.route('/add_to_favorites', methods=["POST"])
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
        return redirect(url_for("create_account", username=username))

    flash('Invalid or expired verification link.')
    return redirect(url_for("verify", username=username))

# Lizeth
def send_verification(email, username, token):
    # Sends Verification Email from the Hangogo Verification email. The email contains unique link to verify a users account. 
    msg = Message('Verify Your Email - Hangogo', sender = 'hangogo.verify@gmail.com' ,recipients=[email])
    verification_link = url_for('verify', username=username,token=token, _external=True)
    msg.body = f'Hi! I cant wait to be friends! Click the following link to verify your email: {verification_link}'

    try:
        mail.send(msg)
        print("Email Sent!")
    except Exception as e:
        flash(f"Failed to send email. Error: {str(e)}")

    return "Verification email sent"

# Lizeth
load_dotenv()
#this is a SMTP Server used for gmail - This connects to the server and sends out the verification email 
app.config['MAIL_SERVER']= os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Lizeth
@app.route('/update-user', methods=['POST'])
def update_user():
    try:
        # Get data from the AJAX request
        data = request.get_json()
        user_id = data.get('userId')
        updated_details = data.get('updatedDetails')

        # Update user details in MongoDB
        users_collection.update_one({'_id': user_id}, {'$set': updated_details})

        # Return the updated user details as a response
        updated_user = users_collection.find_one({'_id': user_id})
        return jsonify(updated_user)

    except Exception as e:
        print(f"Error updating user details: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    



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
@app.route("/favorites", methods=["GET"])
def favorites():
    user = session.get("user")
    if user is None:
        flash("Please log in to access favorites page.")
        return redirect(url_for("login"))

    user_id = user["_id"]

    query = {"_id" : ObjectId(user_id)}

    user_profile = users_collection.find_one(query)
    
    if user_profile:
        favorite_list = user_profile.get('favorite_list')
        total_places = len(favorite_list)

        # places = places.skip((page - 1) * per_page).limit(per_page)
        page = request.args.get("page", default=1, type=int)
        per_page = 2
        start_index = (page - 1) * per_page
        end_index = min(start_index + per_page, total_places)
        paginated_favorites = favorite_list[start_index:end_index]

        # Retrieve information of each place from places_collection
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
        return render_template("favorites.html", favorites=favorites_info, place=place_info, page=page, per_page=per_page, total_places=total_places)
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
    return jsonify(coordinates)

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

@app.route('/add_another_user_for_rec', methods=['GET'])
def add_another_user_for_rec():
    friends_data = list(users_collection.find({}, {'username':1, 'location':1 }))
    print(friends_data)
    return render_template("add_another_user_for_rec.html", user_data=user_data, friends_data=friends_data)


@app.route('/calculate_center', methods=['POST'])
def calculate_center():
    data = request.json
    locations = data['locations']
    
    # Calculate center location
    # logic here
    
    center_location = {}  # Replace this with your calculated center location
    
    return jsonify(center_location)

# Gloria
# generate recommendation for multiple users placeholder, Nhu will have the alogorithm how it generates the places from the 2 locations
@app.route('/multi_recommendation', methods=['POST'])
def multi_recommendation():
    target_user_id = request.json.get('target_user_id')
    target_location = user_data.get(target_user_id, {}).get('location')
    # Logic to generate recommendations based on target_location
    recommendations = ["user1", "user2"]  # Dummy recommendations
    return jsonify({"recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True)