import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "student_management_secret_key"

# Application version (configurable via environment variable)
APP_VERSION = os.getenv("APP_VERSION", "v1.0.0")

# In-memory storage for simplicity
users = {"admin": "admin123"}  # Pre-registered admin account
attendance_records = [
    {"student_name": "Rahul Sharma", "roll_no": "101", "date": "2026-08-30", "status": "Present"},
    {"student_name": "Priya Patel", "roll_no": "102", "date": "2026-08-30", "status": "Absent"}
]

@app.context_processor
def inject_version():
    return dict(app_version=APP_VERSION)

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password!", "danger")
            
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username in users:
            flash("Username already exists!", "danger")
        elif not username or not password:
            flash("All fields are required!", "danger")
        else:
            users[username] = password
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
            
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"], records=attendance_records)

@app.route("/mark-attendance", methods=["POST"])
def mark_attendance():
    if "username" not in session:
        return redirect(url_for("login"))
        
    student_name = request.form.get("student_name")
    roll_no = request.form.get("roll_no")
    date = request.form.get("date")
    status = request.form.get("status")
    
    if student_name and roll_no and date and status:
        attendance_records.append({
            "student_name": student_name,
            "roll_no": roll_no,
            "date": date,
            "status": status
        })
        flash("Attendance marked successfully!", "success")
    else:
        flash("Please fill all attendance details!", "danger")
        
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)