from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# In-memory storage for demonstration
users = {}
students = [
    {
        'id': '101',
        'name': 'Ananya Rao',
        'email': 'ananya@example.com',
        'phone': '+91 9876543210',
        'department': 'Computer Science',
        'course': 'B.E. CS',
        'admission_date': '2024-08-01'
    },
    {
        'id': '102',
        'name': 'Rahul Sharma',
        'email': 'rahul@example.com',
        'phone': '+91 9876543211',
        'department': 'Information Science',
        'course': 'B.Tech IT',
        'admission_date': '2024-08-02'
    }
]

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        session['user'] = email
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        role = request.form.get('role')
        password = request.form.get('password')
        users[email] = {'name': full_name, 'role': role, 'password': password}
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    total_students = len(students)
    active_courses = len(set(s['course'] for s in students))
    faculty_count = 12
    avg_attendance = "88%"
    
    return render_template('dashboard.html', 
                           students=students, 
                           total_students=total_students,
                           active_courses=active_courses,
                           faculty_count=faculty_count,
                           avg_attendance=avg_attendance,
                           user=session.get('user'))

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        new_student = {
            'id': request.form.get('student_id'),
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'department': request.form.get('department'),
            'course': request.form.get('course'),
            'admission_date': request.form.get('admission_date')
        }
        students.append(new_student)
        return redirect(url_for('dashboard'))
    return render_template('add_student.html')

@app.route('/delete_student/<student_id>')
def delete_student(student_id):
    global students
    students = [s for s in students if s['id'] != student_id]
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)