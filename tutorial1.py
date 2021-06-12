from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import time, timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime= timedelta(days = 5)

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/test")
def test():
    return render_template("template.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))

    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        
        return render_template("login.html")

@app.route("/user", methods = ["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        flash("Login Successful")
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Your email was saved.")
        else:
            if "email" in session:
                email = session["email"]
        
        return render_template("user.html", email = email)
    
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    user = session["user"]
    flash(f"You have been logged out successfully, {user}.", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)