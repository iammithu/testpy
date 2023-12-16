from flask import Flask, render_template, request, redirect, url_for

import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                father_name TEXT,
                age INTEGER,
                phone_number TEXT,
                location TEXT,
                date_of_birth TEXT,
                photo_path TEXT
            )
        ''')
        conn.commit()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Display all students route
@app.route('/display_students')
def display_students():
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students')
        students = cursor.fetchall()

    return render_template('display_students.html', students=students)

# Display individual student route
@app.route('/display_student/<int:student_id>')
def display_student(student_id):
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()

    return render_template('display_student.html', student=student)

# Form submission route
@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    name = request.form['name']
    father_name = request.form['father_name']
    age = request.form['age']
    phone_number = request.form['phone_number']
    location = request.form['location']
    date_of_birth = request.form['date_of_birth']
    # You can handle the photo upload here and save the file path in the database

    # Insert data into the database
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (name, father_name, age, phone_number, location, date_of_birth)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, father_name, age, phone_number, location, date_of_birth))
        conn.commit()

    return redirect(url_for('home'))

# Edit student route
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            # Update student data in the database
            cursor.execute('''
                UPDATE students
                SET name=?, father_name=?, age=?, phone_number=?, location=?, date_of_birth=?
                WHERE id=?
            ''', (
                request.form['name'],
                request.form['father_name'],
                request.form['age'],
                request.form['phone_number'],
                request.form['location'],
                request.form['date_of_birth'],
                student_id
            ))
            conn.commit()

            return redirect(url_for('display_students'))
        else:
            # Fetch the existing student data for editing
            cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
            student = cursor.fetchone()

    return render_template('edit_student.html', student=student)

# Delete student route
@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()

    return redirect(url_for('display_students'))


# Run the application
if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
