# For my personal touch, I implemented deposit (letting users add more cash to their account)

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        # Checks if symbol and shares were inputted
        if not request.form.get("symbol"):
            return apology("Input a symbol.")
        elif not request.form.get("shares"):
            return apology("Input shares.")
        # Checks if shares is a digit
        elif not request.form.get("shares").isdigit():
            return apology("Shares must be a number.")

        shares = int(request.form.get("shares"))
        if not shares:
            return apology("Error processing shares.")

        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Symbol is invalid.")

        cost = shares * quote["price"]
        rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        if not rows:
            return apology("User is not in system.")

        cash = rows[0]["cash"]
        if cash < cost:
            return apology("Not enough cash to make this purchase.")

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], quote["symbol"], shares, quote["price"])
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])

        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # check if they inputted a symbol
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Input a symbol.")

        # check whether the symbol was valid
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Symbol is invalid.")

        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("Input a symbol.")
        elif not request.form.get("shares"):
            return apology("Input shares.")
        # Checks if shares is a digit
        elif not request.form.get("shares").isdigit():
            return apology("Shares must be a number.")

        shares = int(request.form.get("shares"))
        if not shares:
            return apology("Error processing shares.")

        symbol = request.form.get("symbol").upper()

        # Checks how many shares the user owns
        rows = db.execute(
            "SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", session["user_id"], symbol)

        if len(rows) != 1:
            return apology("No stock is owned.")

        if shares > rows[0]["shares"]:
            return apology("Can not sell more stock than is owned.")

        quote = lookup(request.form.get("symbol"))

        db.execute("INSERT INTO transactions (user_id, symbol, price, shares) VALUES (?, ?, ?, ?)",
                   session["user_id"], quote["symbol"], quote["price"], -shares)
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", shares * quote["price"], session["user_id"])

        flash("Sold!")
        return redirect("/")

    else:
        stocks = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        return render_template("sell.html", stocks=stocks)


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Add cash to account"""

    if request.method == "POST":

        # Checks if cash amount was inputted
        if not request.form.get("cashAmount"):
            return apology("Input a cash amount.")

        # Checks if shares is a digit
        elif not request.form.get("cashAmount").isdigit():
            return apology("Cash amount must be a number.")

        cashAmount = int(request.form.get("cashAmount"))
        if not cashAmount:
            return apology("Error processing cash amount.")

        rows = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        if not rows:
            return apology("User is not in system.")

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", cashAmount, session["user_id"])

        flash("Deposited!")
        return redirect("/")

    else:
        return render_template("deposit.html")