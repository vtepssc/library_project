from flask import Flask, render_template
from flask_login import LoginManager
from flask_login import UserMixin

from flask import request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash


import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


# --- Flask-Login setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."


class User(UserMixin):
    def __init__(self, user_id, username, password_hash, first_name, last_name, email, phone):
        self.id = user_id   # Flask-Login expects an "id" attribute
        self.username = username
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

@login_manager.user_loader
def load_user(user_id):
    import sqlite3
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return User(
            row["user_id"],
            row["username"],
            row["password_hash"],
            row["first_name"],
            row["last_name"],
            row["email"],
            row["phone"]
        )
    return None



# login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # fetch user from database
        conn = sqlite3.connect("library.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            # create User object with all required fields
            user = User(
                row["user_id"],
                row["username"],
                row["password_hash"],
                row["first_name"],
                row["last_name"],
                row["email"],
                row["phone"]
            )
            if check_password_hash(row["password_hash"], password):
                login_user(user)
                return redirect(url_for("index"))
        
        flash("Invalid username or password")
    return render_template("login.html")


# logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))




@app.route("/")
@login_required
def index():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return render_template("index.html", books=books)


if __name__ == "__main__":
    app.run(debug=True)
