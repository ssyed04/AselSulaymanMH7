#main.py

from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import time, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import expression


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
    word = db.Column(db.String(100), nullable=False)
    #track_weight = db.Column(db.Boolean, unique=False, nullable=False)
    tracks = db.Column(db.String(100))
    knowledge = db.Column(db.String(100))
    equipment = db.Column(db.String(100))
    
    def __init__(self, name, email, password, track_weight):
        self.name = name
        self.email = email
        self.word = password
        self.tracks = "_"
        self.knowledge = "_"
        self.equipment = "_"
        #self.track_weight = track_weight

    def getTracks(self, arg1, arg2, arg3):
        self.tracks += setChar(arg1)
        self.tracks += setChar(arg2)
        self.tracks += setChar(arg3)

    def getKnowledge(self, arg1, arg2, arg3):
        self.knowledge += setChar(arg1)
        self.knowledge += setChar(arg2)
        self.knowledge += setChar(arg3)

    def getEquipment(self, arg1, arg2, arg3, arg4, arg5, arg6):
        self.equipment += setChar(arg1)
        self.equipment += setChar(arg2)
        self.equipment += setChar(arg3)
        self.equipment += setChar(arg4)
        self.equipment += setChar(arg5)
        self.equipment += setChar(arg6)
        

def setChar(bool):
    if bool:
        return "Y"
    else:
        return "N"
    
@app.route("/")
def home():
    return render_template("homepage.html")

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

        track_weight = 'track_weight' in request.form and request.form["track_weight"] == "on"
        track_PRs = 'track_PRs' in request.form and request.form["track_PRs"] == "on"
        track_macros = 'track_macros' in request.form and request.form["track_macros"] == "on"
        session["track_weight"] = track_weight
        session["track_PRs"] = track_PRs
        session["track_macros"] = track_macros
        
        is_beginner = 'is_beginner' in request.form and request.form["is_beginner"] == "on"
        is_mid = 'is_mid' in request.form and request.form["is_mid"] == "on"
        is_pro = 'is_pro' in request.form and request.form["is_pro"] == "on"
        #is_beginner = request.form["is_beginner"] == "on"
        #is_mid = request.form["is_mid"] == "on"
        #is_pro = request.form["is_pro"] == "on"
        session["is_beginner"] = is_beginner
        session["is_mid"] = is_mid
        session["is_pro"] = is_pro

        has_rack = 'has_rack' in request.form and request.form["has_rack"] == "on"
        has_barbell = 'has_barbell' in request.form and request.form["has_barbell"] == "on"
        has_dbs = 'has_dbs' in request.form and request.form["has_dbs"] == "on"
        has_bands = 'has_bands' in request.form and request.form["has_bands"] == "on"
        has_treadmill = 'has_treadmill' in request.form and request.form["has_treadmill"] == "on"
        has_eliptical = 'has_eliptical' in request.form and request.form["has_eliptical"] == "on"
        #has_rack = request.form["has_rack"] == "on"
        #has_barbell = request.form["has_barbell"] == "on"
        #has_dbs = request.form["has_dbs"] == "on"
        #has_bands = request.form["has_bands"] == "on"
        #has_treadmill = request.form["has_treadmill"] == "on"
        #has_eliptical = request.form["has_eliptical"] == "on"
        session["has_rack"] = has_rack
        session["has_barbell"] = has_barbell
        session["has_dbs"] = has_dbs
        session["has_bands"] = has_bands
        session["has_treadmill"] = has_treadmill
        session["has_eliptical"] = has_eliptical

        
        usr = users(user, email, password, track_weight)
        usr.getTracks(track_weight, track_PRs, track_macros)
        usr.getKnowledge(is_beginner, is_mid, is_pro)
        usr.getEquipment(has_rack, has_barbell, has_dbs, has_bands, has_treadmill, has_eliptical)
        #usr.getKnowledge(is_beginner, is_mid, is_pro)
        #usr.getEquipment(has_rack, has_barbell, has_dbs, has_bands, has_treadmill, has_eliptical)
        db.session.add(usr)
        db.session.commit()
        return redirect(url_for("dashboard"))

    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))
        
        return render_template("signup.html")

@app.route("/dashboard", methods = ["POST", "GET"])
def dashboard():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Your email was saved.")
        else:
            if "email" in session:
                email = session["email"]
        
        return render_template("progress.html", email = email)
    
    else:
        flash("You are not logged in!")
        return redirect(url_for("signup"))

@app.route("/logout")
def logout():
    user = session["user"]
    flash(f"You have been logged out successfully, {user}.", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("signup"))

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        formemail = request.form["email"]
        formpassword = request.form["password"]
        session["entered password"] = formpassword
        session["entered email"] = formemail
        flash(f"password{formemail,formpassword}", "info")        
        found_user = users.query.filter_by(email=formemail).first()
        if found_user:
            app.logger.warning(found_user)
            if found_user.password == formpassword:
                session['user'] = found_user.name
                flash(f"password{formemail,formpassword}", "info")    
                flash("Login Successful!", "info")        
                
                return redirect(url_for("user"))
            else:
                flash("Incorrect credentials. Please try again")
                session.pop("entered password", None)
                session.pop("enteredemail", None)
    return render_template("login.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

#test asel
#test sul
