# app.py
from bson import ObjectId
import json
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session, flash
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

        registration_error = register_user(username, email, password, confirm_password)

        if registration_error is not None:
            print("Registration error:", registration_error)
            # comment out below the one line of code below before presentation and launch
            print("Form values:", username, email, password, confirm_password)
            return render_template("register.html", error=registration_error)

        print("Registration successful. Redirecting to index.")
        return redirect(url_for("create_account"))

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



@app.route("/create-account", methods=["GET", "POST"])
def create_account():
        if request.method == "POST":
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            birth_month = int(request.form.get("birth_month"))
            birth_day = int(request.form.get("birth_day"))
            birth_year = int(request.form.get("birth_year"))

            # Check if the user is at least 13 years old
            age = calculate_age(birth_year, birth_month, birth_day)
            # if age < 13:
            #     return render_template("create-account.html", error = "You must be at least 13 years old")
            
            create_account_error = user_create_account(first_name, last_name, birth_month, birth_day, birth_year, age)
            if create_account_error is not None:
                print("Create account error:", create_account_error)
                print("Form values:", first_name, last_name, birth_month, birth_day, birth_year, age)
                return render_template("create-account.html", error=create_account_error)

            return redirect(url_for("index"))
        return render_template("create-account.html")


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
