from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a strong, unique secret key

# Function to connect to the SQLite database
def connect_db():
    return sqlite3.connect("user_database.db")

# Login route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        emp_code = request.form["emp_code"]
        password = request.form["password"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT emp_code, usertype FROM user_data WHERE emp_code = ? AND password = ?", (emp_code, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["emp_code"] = user[0]
            session["usertype"] = user[1]
            if user[1] == "admin":
                return redirect(url_for("admin_dashboard"))
            elif user[1] == "lineman":
                return redirect(url_for("lineman_dashboard"))
        else:
            flash("Invalid credentials. Please try again.", "error")

    return render_template("login.html")

# Admin dashboard route
@app.route("/admin_dashboard")
def admin_dashboard():
    if "usertype" in session and session["usertype"] == "admin":
        return render_template("admin_dashboard.html")
    else:
        return redirect(url_for("login"))

# Lineman dashboard route
@app.route("/lineman_dashboard")
def lineman_dashboard():
    if "usertype" in session and session["usertype"] == "lineman":
        return render_template("lineman_dashboard.html")
    else:
        return redirect(url_for("login"))

# Logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
