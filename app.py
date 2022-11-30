# For my personal touch, I implemented deposit (letting users add more cash to their account)

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from sqlite3 import Error

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

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


@app.route("/graph")
@login_required
def graph():
    """Show cost per wear graph of closet"""

    clothing = db.execute("SELECT * FROM clothing WHERE user_id = ?", session["user_id"])
    return render_template("graph.html", clothing=clothing)


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
        session["user_id"] = rows[0]["id"]

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

        try:
            id = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get(
                "username"), generate_password_hash(request.form.get("password")))

        except ValueError:
            # username is already taken
            return apology("Username is already taken.")

        session["user_id"] = id

        flash("Registered!")
        return redirect("/")

    else:
        # the method was get
        return render_template("register.html")


@app.route("/addClothing", methods=["GET", "POST"])
@login_required
def addClothing():
    """Add clothing to user's closet"""

    if request.method == "POST":

        if not request.form.get("picture"):
            return apology("Input an image.")
        elif not request.form.get("item_name"):
            return apology("Input item name.")

        # Checks how many shares the user owns
        rows = db.execute(
            "SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", session["user_id"], symbol)

        if len(rows) != 1:
            return apology("No stock is owned.")

        if shares > rows[0]["shares"]:
            return apology("Can not sell more stock than is owned.")

        quote = lookup(request.form.get("symbol"))

        db.execute("INSERT INTO image_uploads (file_name, user_id, item_name) VALUES (?, ?, ?)", request.form.get("picture"),
                   session["user_id"], request.form.get("item_name"))
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", shares * quote["price"], session["user_id"])

        flash("Sold!")
        return redirect("/")

    else:
        stocks = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        return render_template("addClothing.html", stocks=stocks)


@app.route("/closet")
@login_required
def closet():
    """Display user's clothing"""

    picturesDict = db.execute(
        "SELECT * FROM image_uploads WHERE user_id = ?", session["user_id"])

    return render_template("closet.html", picturesDict=picturesDict)