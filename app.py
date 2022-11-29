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

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

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
    """Show portfolio of stocks"""

    rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    if not rows:
        return apology("User is not in system.")

    cash = rows[0]["cash"]
    total = cash

    stocks = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        total += stock["price"] * stock["shares"]

    return render_template("index.html", cash=cash, total=total, stocks=stocks)


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

        db.execute("INSERT INTO image_uploads (file_name, user_id, item_name) VALUES (?, ?, ?)", request.form.get("picture")
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

    rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    if not rows:
        return apology("User is not in system.")

    cash = rows[0]["cash"]
    total = cash

    stocks = db.execute(
        "SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        total += stock["price"] * stock["shares"]

    return render_template("closet.html", cash=cash, total=total, stocks=stocks)


#Function that takes in file path and file blob and commits to database
def insert_into_database(file_path_name, file_blob): 
  try:
    conn = sqlite3.connect('app.db')
    print("[INFO] : Successful connection!")
    cur = conn.cursor()
    sql_insert_file_query = '''INSERT INTO uploads(file_name, file_blob)
      VALUES(?, ?)'''
    cur = conn.cursor()
    cur.execute(sql_insert_file_query, (file_path_name, file_blob, ))
    conn.commit()
    print("[INFO] : The blob for ", file_path_name, " is in the database.") 
    last_updated_entry = cur.lastrowid
    return last_updated_entry
  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()
    else:
      error = "Oh shucks, something is wrong here."

#Create blob data to temporarily store the binary data
def convert_into_binary(file_path):
  with open(file_path, 'rb') as file:
    binary = file.read()
  return binary

#Retrieve the file and view its original form - find the image file in the database and write blob to a file
def read_blob_data(entry_id):
  try:
    conn = sqlite3.connect('app.db')
    cur = conn.cursor()
    print("[INFO] : Connected to SQLite to read_blob_data")
    sql_fetch_blob_query = """SELECT * from uploads where id = ?"""
    cur.execute(sql_fetch_blob_query, (entry_id,))
    record = cur.fetchall()
    for row in record:
      converted_file_name = row[1]
      photo_binarycode  = row[2]
      # parse out the file name from converted_file_name
      # Windows developers should reverse "/" to "\" to match your file path names 
      last_slash_index = converted_file_name.rfind("/") + 1 
      final_file_name = converted_file_name[last_slash_index:] 
      write_to_file(photo_binarycode, final_file_name)
      print("[DATA] : Image successfully stored on disk. Check the project directory. \n")
    cur.close()
  except sqlite3.Error as error:
    print("[INFO] : Failed to read blob data from sqlite table", error)
  finally:
    if conn:
        conn.close()

#To convert binary into a file, pass the blob in as well as the name of the file
def write_to_file(binary_data, file_name):
  with open(file_name, 'wb') as file:
    file.write(binary_data)
  print("[DATA] : The following file has been written to the project directory: ", file_name)

  def main():
    #need to connect inputs to form
    file_path_name = input("Enter full file path:\n") 
    file_blob = convert_into_binary(file_path_name)
    print("[INFO] : the last 100 characters of blob = ", file_blob[:100]) 
    last_updated_entry = insert_into_database(file_path_name, file_blob)
    #retrieving the image from the last entry
    read_blob_data(last_updated_entry)
