import os
import urllib.parse
import requests

from flask import redirect, render_template, session
from werkzeug.security import check_password_hash
from datetime import datetime
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """

        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    if isinstance(message, str):
        message = escape(message)
    else:
        message = "Error occured!"

    return render_template("apology.html", top=code, bottom=message), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated_function



def lookup(symbol):
    """Look up quote for symbol."""
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY not set")

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={api_key}'
    r = requests.get(url)
    data = r.json()

    # بررسی وجود داده‌ها
    if "Time Series (1min)" not in data:
        return None

    # دریافت آخرین قیمت
    time_series = data["Time Series (1min)"]
    latest_time = sorted(time_series.keys())[0]
    latest_data = time_series[latest_time]

    return {
        "name": symbol,
        "price": float(latest_data["1. open"]),
        "symbol": symbol
    }

def usd(value):
    """Format value as USD."""

    return f"${value:,.2f}"


def get_time():
    """Returns formatted local time."""

    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def check_password(first_password, second_password):
    """Checks the passwords to be a match. Returns a message error if they do not match."""

    if not check_password_hash(first_password, second_password):
        return apology("Passwords do not match!", code=401)
