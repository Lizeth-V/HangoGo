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
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        registration_error = register_user(username, email, password, confirm_password)

        if registration_error:
            print("Registration error:", registration_error)
            print("Form values:", username, email, password, confirm_password)
            return render_template("register.html", error=registration_error)

        print("Registration successful. Redirecting to index.")
        return redirect(url_for("index"))

    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
