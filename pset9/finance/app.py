import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Ensure API key is set
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

    # Get user portfolio and cash balance
    portfolio = db.execute("SELECT symbol, shares FROM portfolios WHERE user_id = ?", user_id)
    cash_left = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
    total_value = cash_left

    # Update stock prices and calculate total value
    for stock in portfolio:
        stock_info = lookup(stock["symbol"])
        if stock_info:
            stock["current_price"] = stock_info["price"]
            stock["total_value"] = stock_info["price"] * stock["shares"]
            total_value += stock["total_value"]
        else:
            flash(f"Could not retrieve data for {stock['symbol']}.", "warning")

    return render_template("index.html", portfolio=portfolio, cash_left=cash_left, total_value=total_value)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate form inputs
        if not username or not password or not confirmation:
            return apology("All fields are required!", 400)

        # Ensure username is unique
        if db.execute("SELECT id FROM users WHERE username = ?", username):
            return apology("Username already exists!", 400)

        # Check if passwords match
        if password != confirmation:
            return apology("Passwords must match!", 400)

        hashed_password = generate_password_hash(password)

        # Try to insert user
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)
        except Exception as e:
            print(f"Database error: {e}")
            return apology("Registration failed. Please try again.", 500)

        # Log user in
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        session["user_id"] = user_id
        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("Must provide username and password!", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Invalid username and/or password!", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Must provide stock symbol!", 400)

        try:
            stock = lookup(symbol)
            if not stock:
                return apology("Invalid stock symbol!", 400)
            print(f"Stock found: {stock}")  # برای دیباگ
        except Exception as e:
            print(f"Error fetching stock info: {e}")
            return apology("Error retrieving stock information.", 500)

        return render_template("quoted.html", stock=stock)

    return render_template("quote.html")



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate inputs
        if not symbol or not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid input!", 400)

        shares = int(shares)
        stock = lookup(symbol)
        if not stock:
            return apology("Invalid stock symbol!", 400)

        cost = shares * stock["price"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        if cost > user_cash:
            return apology("Not enough cash!", 400)

        # Update database
        try:
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                       session["user_id"], symbol, shares, stock["price"])
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])
        except Exception as e:
            print(f"Database error: {e}")
            return apology("Transaction failed. Please try again.", 500)

        flash(f"Bought {shares} shares of {symbol} for {usd(cost)}!", "success")
        return redirect("/")


    return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Validate inputs
        if not symbol or not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid input!", 400)

        shares = int(shares)
        stock = lookup(symbol)
        if not stock:
            return apology("Invalid stock symbol!", 400)

        user_shares = db.execute("SELECT shares FROM portfolios WHERE user_id = ? AND symbol = ?",
                                 session["user_id"], symbol)
        if not user_shares or user_shares[0]["shares"] < shares:
            return apology("Not enough shares!", 400)

        # Update database
        revenue = shares * stock["price"]
        try:
            db.execute("UPDATE portfolios SET shares = shares - ? WHERE user_id = ? AND symbol = ?",
                       shares, session["user_id"], symbol)
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", revenue, session["user_id"])
        except Exception as e:
            print(f"Database error: {e}")
            return apology("Transaction failed. Please try again.", 500)

        flash("Sold successfully!")
        return redirect("/")

    symbols = db.execute("SELECT symbol FROM portfolios WHERE user_id = ?", session["user_id"])
    return render_template("sell.html", symbols=[row["symbol"] for row in symbols])


@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/withdraw")
@login_required
def withdraw():
    return render_template("withdraw.html")

@app.route("/deposit")
@login_required
def deposit():
    return render_template("deposit.html")
