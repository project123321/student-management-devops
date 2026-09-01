from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey123'

# In-memory user credentials (Name & Password as requested)
users = {"admin": "password123"}

# Student records
students = [
    {"id": 1, "name": "Swathi Mankani", "roll": "101", "date": "2026-09-01", "attendance": "Present", "marks": 85, "grade": "A"},
    {"id": 2, "name": "Rahul Sharma", "roll": "102", "date": "2026-09-01", "attendance": "Absent", "marks": 42, "grade": "F"}
]

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            error = "Invalid Name or Password!"
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if username in users:
            error = "Name already exists!"
        elif password != confirm_password:
            error = "Passwords do not match!"
        elif username and password:
            users[username] = password
            return redirect(url_for('login'))
        else:
            error = "Please fill in all fields."
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    total_students = len(students)
    present_count = sum(1 for s in students if s['attendance'] == 'Present')
    absent_count = sum(1 for s in students if s['attendance'] == 'Absent')

    return render_template('dashboard.html', 
                           students=students, 
                           total=total_students, 
                           present=present_count, 
                           absent=absent_count)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        roll = request.form.get('roll')
        date = request.form.get('date') or datetime.now().strftime('%Y-%m-%d')
        marks = request.form.get('marks', 0)
        attendance = request.form.get('attendance', 'Present')

        try:
            marks = int(marks)
        except ValueError:
            marks = 0

        # Feature 2: Automated Grade Calculation
        if marks >= 85:
            grade = 'A+'
        elif marks >= 70:
            grade = 'A'
        elif marks >= 50:
            grade = 'B'
        elif marks >= 35:
            grade = 'C'
        else:
            grade = 'F'

        if name and roll:
            new_id = max([s['id'] for s in students], default=0) + 1
            students.append({
                "id": new_id,
                "name": name,
                "roll": roll,
                "date": date,
                "attendance": attendance,
                "marks": marks,
                "grade": grade
            })
            return redirect(url_for('index'))

    today_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('add_student.html', today_date=today_date)

@app.route('/toggle_attendance/<int:student_id>')
def toggle_attendance(student_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    for student in students:
        if student['id'] == student_id:
            student['attendance'] = "Absent" if student['attendance'] == "Present" else "Present"
            break
    return redirect(url_for('index'))

@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    global students
    students = [s for s in students if s['id'] != student_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)