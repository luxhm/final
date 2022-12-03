from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import base64
import os
from sqlite3 import Error

from helpers import apology, login_required

# Configure application
app = Flask(__name__)
app.jinja_env.filters["b64encode"] = lambda b: base64.b64encode(b).decode("ascii")


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///app.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show home page"""
    
    return render_template("index.html")


@app.route("/table")
@login_required
def table():
    """Show cost per wear table for closet"""

    clothing = db.execute("SELECT * FROM image_uploads WHERE user_id = ?", session["user_id"])
    return render_template("table.html", clothing=clothing)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # check if they inputted a username
        if not request.form.get("username"):
            return apology("Input a username.")
        # check if they inputted a password
        elif not request.form.get("password"):
            return apology("Input a password.")
        # check if password and confirmation are the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Confirmation does not match the password.")

        #Insert registered user into users database
        try:
            id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get(
                "username"), generate_password_hash(request.form.get("password")))

        except ValueError:
            # username is already taken
            return apology("Username is already taken.")

        session["user_id"] = id
        return redirect("/")

    else:
        # the method was get
        return render_template("register.html")


@app.route("/addClothing", methods=["GET", "POST"])
@login_required
def addClothing():
    """Add clothing to user's closet"""

    #Check user inputted an image, image name, and cost
    if request.method == "POST":

        if not request.files["picture"]:
            return apology("Input an image.")
        if not request.form.get("item_name"):
            return apology("Input item name.")
        if not request.form.get("cost"):
            return apology("Input item cost.")

        #Request file uploaded by user
        filename = request.files["picture"].filename

        #Read uploaded file to variable
        file = request.files["picture"].read()

        #Adding uploaded image to database
        db.execute(""" INSERT INTO image_uploads
                (file_name, user_id, item_name, file_blob, cost)
                VALUES (?, ?, ?, ?, ?)""",
               filename, session["user_id"], request.form.get("item_name"), file,  request.form.get("cost"))
        
        #Redirect to upload page
        return redirect("/closet")

    else:
        return render_template("addClothing.html")


@app.route("/closet", methods=["GET", "POST"])
@login_required
def closet():
    """Display user's clothing and update count"""

    #Get count from form upload
    if request.method == "POST":
        if not request.form.get("count"):
            return apology("Input a number.")
        #Update the count in image_uploads 
        db.execute("UPDATE image_uploads SET count = ? WHERE id = ?", request.form.get("count"), request.form.get("image_id"))
        return redirect("/closet")

    #Select user's uploaded images
    else:
        picturesDict = db.execute(
            "SELECT * FROM image_uploads WHERE user_id = ?", session["user_id"])

        return render_template("closet.html", picturesDict=picturesDict)