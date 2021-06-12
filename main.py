from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import time, timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime= timedelta(days = 5)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        

    

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/view")
def view():
    return render_template("view.html", values = users.query.all())


@app.route("/signup", methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        email= request.form["email"]
        session["email"] = email
        password = request.form["password"]
        session["password"] = password

        usr = users(user, email, password)
        db.session.add(usr)
        db.session.commit()
        return redirect(url_for("user"))

    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        
        return render_template("signup.html")

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
    return redirect(url_for("signup"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

#test asel
#test sul
