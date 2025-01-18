import re
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import apology, login_required, lookup, usd, get_time
from flask_session import Session

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
    """Show portfolio of stocks."""
    user_id = session["user_id"]

    # Get user portfolio
    portfolio = db.execute("SELECT * FROM portfolios WHERE user_id = ?", user_id)

    # Get user's cash balance
    cash_left = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    if not cash_left or "cash" not in cash_left[0]:
        cash_left = 0.0
    else:
        cash_left = float(cash_left[0]["cash"])

    total_amount = cash_left

    # Update stock prices and calculate total value
    if portfolio:
        for stock in portfolio:
            symbol = stock["symbol"]
            stock_info = lookup(symbol)
            if not stock_info:
                return apology(f"Could not fetch data for {symbol}", 400)

            current_price = float(stock_info["price"])
            stock_value = current_price * stock["shares"]
            stock.update({"current_price": current_price, "stock_value": stock_value})
            total_amount += stock_value
    else:
        portfolio = []

    return render_template("index.html", portfolio=portfolio, cash_left=cash_left, total_amount=total_amount)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check for empty fields
        if not username or not password or not confirmation:
            return apology("Fields cannot be empty!", 400)

        # Validate username
        if len(username) < 4:
            return apology("Username must be at least 4 characters long!", 400)
        if not username.isalnum():
            return apology("Username must contain only letters and numbers!", 400)

        # Validate password
        if len(password) < 8:
            return apology("Password must be at least 8 characters long!", 400)
        if (not re.search("[a-zA-Z]", password) or
            not re.search("[0-9]", password) or
            not re.search("[!@#$%^&*()]", password)):
            return apology("Password must include letters, numbers, and symbols!", 400)

        # Check password confirmation
        if password != confirmation:
            return apology("Passwords do not match!", 400)

        try:
            # Ensure username is unique
            if db.execute("SELECT id FROM users WHERE username = ?", username):
                return apology("Username already exists!", 400)

            hashed_password = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

            # Log the user in
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            session["user_id"] = rows[0]["id"]

            return redirect("/")
        except Exception as e:
            print(f"Error during registration: {e}")
            return apology("An error occurred during registration.", 500)

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("Must provide username!", 403)
        if not password:
            return apology("Must provide password!", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""
    session.clear()
    return redirect("/")


# Additional routes remain unchanged
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid symbol!", 400)
        stock["price"] = usd(stock["price"])
        return render_template("quoted.html", stock=stock)
    return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        # Implementation remains the same
        pass
    return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "POST":
        # Implementation remains the same
        pass
    return render_template("sell.html")
