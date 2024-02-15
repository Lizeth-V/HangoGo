# app.py
from bson import ObjectId
import json
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
import random
import string
from datetime import datetime, timedelta

from register import register_user, hash_password
from create_account import user_create_account, calculate_age
from db import users_collection

app = Flask(__name__)

# secret key
app.secret_key = "supersecrethangogo!!!!"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        #email verification token generated (Lizeth)
        verification_token = ''.join(random.choices(string.ascii_letters + string.digits, k=30))

        registration_error = register_user(username, email, password, confirm_password, verification_token)

        if registration_error is not None:
            print("Registration error:", registration_error)
            # comment out below the one line of code below before presentation and launch
            print("Form values:", username, email, password, confirm_password)
            return render_template("register.html", error=registration_error)
        
        # sending email verifcation 
        send_verification(email, username, verification_token)

        print("Registration successful. Redirecting to verify email.")
        return redirect(url_for("verify", username=username, token=verification_token))

    return render_template("register.html")

@app.route("/login", methods= ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = users_collection.find_one({"username": username})

        if user:
            # Get the hashed password from the user object
            hashed_password = user["password"]

            # check if the password the user entered matches the hashed password
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                # password is matched
                # convert ObjectId to string for JSON serialization
                user["_id"] = str(user["_id"])
                session["user"] = user
                print("Login Success")
                return redirect(url_for("index"))
            else:
                # password did not match
                print("Invalid username or password")

        else:
            # User not found
            print("User not found.")
    return render_template("login.html")


@app.route("/create-account/<username>", methods=["GET", "POST"])
def create_account(username):
        if request.method == "POST":
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            birth_month = int(request.form.get("birth_month"))
            birth_day = int(request.form.get("birth_day"))
            birth_year = int(request.form.get("birth_year"))

            # Check if the user is at least 13 years old
            age = calculate_age(birth_year, birth_month, birth_day)
            if age < 13:
                return render_template("create-account.html", error = "You must be at least 13 years old")
            
            create_account_error = user_create_account(first_name, last_name, birth_month, birth_day, birth_year, age)
            if create_account_error is not None:
                print("Create account error:", create_account_error)
                print("Form values:", first_name, last_name, birth_month, birth_day, birth_year, age)
                return render_template("create-account.html", error=create_account_error)

            # if "first_name" not in request.form or "last_name" not in request.form or \
            #     "birth_month" not in request.form or "birth_day" not in request.form or \
            #     "birth_year" not in request.form:
            #         return render_template("create-account.html", error="Incomplete form data")


            return redirect(url_for("index"))
        return render_template("create-account.html", username=username)


@app.route("/")
def index():
    return render_template("index.html")

# Sending Email Verifications (Lizeth)

@app.route("/verify/<username>/<token>")
def verify(username, token):
    print("verify page")
    user = users_collection.find_one({'username': username,'verification_token': token, 'token_expiration': {'$gt': datetime.utcnow()}})

    if user:
        # Mark user as verified in the database
        users_collection.update_one({'_id': user['_id']}, {'$set': {'verified': True}})

        flash('Email verification successful! You can now log in.')
        return redirect(url_for("create_account", username=username))

    flash('Invalid or expired verification link.')
    return render_template("verify.html")

def send_verification(email,username, token):
    # sender =['letshangogo@gmail.com']
    msg = Message('Verify Your Email - Hangogo', sender = 'hangogo.verify@gmail.com' ,recipients=[email])
    verification_link = url_for('verify', username=username,token=token, _external=True)
    msg.body = f'Hi! I cant wait to be friends! Click the following link to verify your email: {verification_link}'

    try:
        mail.send(msg)
    except Exception as e:
        flash(f"Failed to send email.")

    return "Verification email sent"

load_dotenv()
#this is a SMTP Server used for gmail
app.config['MAIL_SERVER']= os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
 
mail = Mail(app)

if __name__ == "__main__":
    app.run(debug=True)
