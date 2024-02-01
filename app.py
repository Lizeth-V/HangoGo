# app.py

from flask import Flask, render_template, request, redirect, url_for
from register import register_user

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form.get("username")
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        age = request.form.get("age")
        street = request.form.get("address.street")
        city = request.form.get("address.city")
        state = request.form.get("address.state")
        zip_code = request.form.get("address.zip_code")
        country = request.form.get("address.country")

        registration_error = register_user(uname, email, password, confirm_password)

        if registration_error:
            return render_template("register.html", error=registration_error)

        return redirect(url_for("index"))

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
