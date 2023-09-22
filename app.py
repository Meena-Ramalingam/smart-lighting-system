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

# Form route
@app.route("/form")
def form():
    return render_template("form.html")

# Form submission route
@app.route("/submit", methods=["POST"])
def submit():
    pole_no = request.form.get("pole_no")
    area = request.form.get("area")
    time = request.form.get("time")
    date = request.form.get("date")
    error_code = request.form.get("error_code")
    error_type = request.form.get("error_type")
    is_pending = request.form.get("is_pending")

    conn = sqlite3.connect("smart_lighting_system.db")
    cursor = conn.cursor()

    # Insert the form data into the database
    cursor.execute("INSERT INTO smart_lighting_data (pole_no, area, time, date, error_code, error_type,is_pending) VALUES (?, ?, ?, ?, ?, ?,?)",
                   (pole_no, area, time, date, error_code, error_type, is_pending))
    conn.commit()
    conn.close()

    return redirect(url_for("form"))

# Route to display pending works and update status
@app.route("/pending_works", methods=["GET", "POST"])
def pending_works():
    if request.method == "POST":
        work_id = request.form.get("work_id")
        if "mark_done" in request.form:
            conn = sqlite3.connect("smart_lighting_system.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE smart_lighting_data SET is_pending = ? WHERE id = ?", ("done", work_id))
            conn.commit()
            conn.close()
    
    conn = sqlite3.connect("smart_lighting_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM smart_lighting_data WHERE is_pending = ?", ("pending",))
    pending_works = cursor.fetchall()
    conn.close()

    return render_template("pending_works.html", pending_works=pending_works)

# Logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
