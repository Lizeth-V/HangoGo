# app.py

from flask import Flask, render_template, request, redirect, url_for
from register import register_user
from create_account import user_create_account, calculate_age

app = Flask(__name__)

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
            print("Form values:", username, email, password, confirm_password)
            return render_template("register.html", error=registration_error)

        print("Registration successful. Redirecting to index.")
        return redirect(url_for("index"))

    return render_template("register.html")

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
