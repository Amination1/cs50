from cs50 import SQL
from functools import wraps
from flask import redirect, render_template, request, session
import requests
import os

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message), code

def login_required(f):
    """Decorator to require login for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up stock quote from Alpha Vantage."""
    # API Key for Alpha Vantage (you need to sign up for your own)
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY not set")

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey=T03V8RIEYOKUFQQD"

    try:
        response = requests.get(url)
        data = response.json()

        # Check if the symbol is valid
        if "Time Series (Daily)" not in data:
            return None

        # Get the most recent price
        latest_data = list(data["Time Series (Daily)"].values())[0]
        price = float(latest_data["4. close"])

        return {
            "symbol": symbol.upper(),
            "price": price
        }
    except Exception as e:
        return None



def usd(value):
    """Convert a value into a string with a dollar sign."""
    if value is None:
        value = 0  # If value is None, use 0 as a fallback
    try:
        return f"${value:,.2f}"  # Format as currency
    except (ValueError, TypeError):
        return "$0.00"  # Return a default value if formatting fails
