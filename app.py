import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    # Forget any user_id
    session.clear()

    # Submitting user's input via POST (When user presses enter key or submit button)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # If user left username/password blank
        if username == "":
            return apology("Missing username!", 400)
        if password == "":
            return apology("Missing password!", 400)
        # If user did not enter same password
        elif password != confirmation:
            return apology("Password don't match!", 400)

        # Registering username and password in SQL users database
        check_username = db.execute("SELECT * FROM users WHERE username = ?", username)
        # Checking whether there is existing username already
        if len(check_username) != 0:
            return apology("Username already exists!", 400)

        # If not, insert username and password into SQL users database
        db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)",
            username,
            generate_password_hash(password),
        )

        # Return to login page
        return redirect("/")

    # User reached route via GET (Click on register link)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username!", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password!", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("Invalid username and/or password!", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page (index.html)
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form (login.html)
    return redirect("/")


# After user logged in
@app.route("/")
@login_required
def index():
    # Get username of logged in user
    username = db.execute(
        "SELECT username FROM users WHERE id = ?", session["user_id"]
    )[0]["username"]
    return render_template("index.html", username=username)


# Brings user to webpage to set/change budget
@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    # User reached route via POST
    if request.method == "POST":
        budget = request.form.get("budget")
        # If user submits empty budget value
        if budget == "":
            return apology("Missing Budget Value!", 403)
        # If user submits value that is not integer
        try:
            budget = float(budget)
        except:
            return apology("Budget must be a number!", 403)
        # If user submits negative integer
        if budget < 0:
            return apology("Budget must be positive!", 403)

        # Set temporary value for budget (For flash function below)
        tmp = budget

        # User's current budget (NULL or a number)
        current_budget = db.execute(
            "SELECT budget FROM users WHERE id = ?", session["user_id"]
        )[0]["budget"]
        # User's initial budget set (No change)
        initial_budget = db.execute(
            "SELECT const_budget FROM users WHERE id = ?", session["user_id"]
        )[0]["const_budget"]
        # If valid budget value added, update user's budget in SQL table if user have not set a budget value before
        if current_budget == None:
            db.execute(
                "UPDATE users SET budget = ?, const_budget = ? WHERE id = ?",
                budget,
                budget,
                session["user_id"],
            )

        # If user already has a set budget value
        else:
            expense = initial_budget - current_budget
            # Update const_budget first
            db.execute(
                "UPDATE users SET const_budget = ? WHERE id = ?",
                budget,
                session["user_id"],
            )
            # Budget set - all previous expenditures by users
            budget = budget - expense
            db.execute(
                "UPDATE users SET budget = ? WHERE id = ?", budget, session["user_id"]
            )

        # Show user what budget value he set
        flash(f"Set ${round(tmp, 2)} as monthly budget")
        # Bring user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("budget.html")


# Brings user to history webpage
@app.route("/history")
@login_required
def history():
    # Get current budget of logged in user
    budget = db.execute("SELECT budget FROM users WHERE id = ?", session["user_id"])[0][
        "budget"
    ]

    # Get user's expense amount, cause of expenditure, and date of expenditure. Returns a table with columns of stock symbol and total_shares, earliest expenditure at the top of the table
    expenses = db.execute(
        "SELECT reason, date, expense as cost FROM expenses WHERE user_id = ? ORDER BY date DESC LIMIT 10;",
        session["user_id"],
    )

    # Notify user budget limit exceeded
    if budget < 0:
        flash(f"User has exceeded monthly budget!")

    return render_template("history.html", budget=budget, expenses=expenses)


@app.route("/expense", methods=["GET", "POST"])
@login_required
def expense():
    if request.method == "POST":
        expense = request.form.get("expense")
        reason = request.form.get("reason")

        # If user submits empty expense value
        if expense == "":
            return apology("Missing Expenditure Value!", 403)
        # If user submits value that is not integer
        try:
            expense = float(expense)
        except:
            return apology("Expenditure must be a number!", 403)
        # If user submits negative integer
        if expense < 0:
            return apology("Expenditure must be positive!", 403)

        # User does not submit a reason
        if reason == "":
            return apology("Missing cause of expenditure!", 403)

        # Get user's budget
        budget = db.execute(
            "SELECT budget FROM users WHERE id = ?", session["user_id"]
        )[0]["budget"]

        # If user have not set budget yet
        if budget == None:
            return apology("User have not set budget value yet!", 403)

        # Getting the date of when expense recorded
        date = datetime.datetime.now()

        # Update user's budget amount
        db.execute(
            "UPDATE users SET budget = budget - ? WHERE id = ?",
            expense,
            session["user_id"],
        )

        # Insert Expense amount, cause of expenditure and date into expense table
        db.execute(
            "INSERT INTO expenses (user_id, expense, reason, date) VALUES (?, ?, ?, ?)",
            session["user_id"],
            expense,
            reason,
            date,
        )

        # Show user expenditure and cause of expenditure when button is clicked
        flash(f"Spent ${round(expense, 2)} on {reason}.")
        # Bring user to home page
        return redirect("/history")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("expense.html")
