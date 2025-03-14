import csv
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def authenticate():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()

        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the credentials are valid
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            # Redirect to index.html on successful login
            return redirect('/index')
        else:
            # Handle invalid credentials
            return "Invalid username or password"

@app.route('/create_account', methods=['POST'])
def create_account():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()

        new_username = request.form.get('new_username')
        new_password = request.form.get('new_password')

        # Check if the username is already taken
        cursor.execute("SELECT * FROM users WHERE username = ?", (new_username,))
        existing_user = cursor.fetchone()
        if existing_user:
            # Handle username already taken
            return "Username already taken. Please choose a different username."
        else:
            # Insert the new user into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
            conn.commit()

            # Redirect to index.html on successful account creation
            return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        range_start = int(request.form.get('range_start'))
        range_end = int(request.form.get('range_end'))

        # Perform filtering logic here using range_start and range_end variables
        # Read data from CSV file
        data = []
        with open('data.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)

        # Filter the data based on GradeID range
        filtered_data = []
        for row in data:
            grade_id = row['GradeID']
            if grade_id.startswith('G-'):
                grade_id = grade_id[2:]
            try:
                grade_id = int(grade_id)
                if range_start <= grade_id <= range_end:
                    filtered_data.append(row)
            except ValueError:
                continue

        if 'latest_users' in request.args:
            # Get the latest users from the data
            latest_users = filtered_data[-20:]  # to display the 20 most recently added users
            return render_template('index.html', data=latest_users, range_start=range_start, range_end=range_end, latest_users=True)
        else:
            return render_template('index.html', data=filtered_data, range_start=range_start, range_end=range_end)

    # For GET request or initial rendering, use default filter range of 0-25
    range_start = 0
    range_end = 25

    # Read data from CSV file
    data = []
    with open('data.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row)

    if 'latest_users' in request.args:
        # Get the latest users from the data
        latest_users = data[-20:]  # Display the 20 most recently added users
        return render_template('index.html', data=latest_users, range_start=range_start, range_end=range_end, latest_users=True)
    else:
        # Filter the data based on GradeID range
        filtered_data = []
        for row in data:
            grade_id = row['GradeID']
            if grade_id.startswith('G-'):
                grade_id = grade_id[2:]
            try:
                grade_id = int(grade_id)
                if range_start <= grade_id <= range_end:
                    filtered_data.append(row)
            except ValueError:
                continue

        return render_template('index.html', data=filtered_data, range_start=range_start, range_end=range_end)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        gender = request.form.get('gender')
        nationality = request.form.get('nationality')
        place_of_birth = request.form.get('place_of_birth')
        stage_id = request.form.get('stage_id')
        grade_id = request.form.get('grade_id')
        section_id = request.form.get('section_id')
        topic = request.form.get('topic')
        semester = request.form.get('semester')
        relation = request.form.get('relation')
        raised_hands = request.form.get('raised_hands')
        visited_resources = request.form.get('visited_resources')
        announcements_view = request.form.get('announcements_view')
        discussion = request.form.get('discussion')
        parent_answering_survey = request.form.get('parent_answering_survey')
        parent_school_satisfaction = request.form.get('parent_school_satisfaction')
        student_absence_days = request.form.get('student_absence_days')
        class_label = request.form.get('class')

        # Save the registration details to data.csv file
        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([gender, nationality, place_of_birth, stage_id, grade_id, section_id, topic, semester,
                             relation, raised_hands, visited_resources, announcements_view, discussion,
                             parent_answering_survey, parent_school_satisfaction, student_absence_days, class_label])

        return redirect('/index')

    return render_template('registration.html')

@app.route('/courses')
def courses():
    # Retrieve course data from the database or any other source
    courses = [
        {'name': 'Course 1', 'description': 'Description 1', 'prerequisites': 'Prerequisites 1', 'available_seats': 20},
        {'name': 'Course 2', 'description': 'Description 2', 'prerequisites': 'Prerequisites 2', 'available_seats': 15},
        {'name': 'Course 3', 'description': 'Description 3', 'prerequisites': 'Prerequisites 3', 'available_seats': 10},
    ]
    return render_template('courses.html', courses=courses)

@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        course_name = request.form.get('name')
        description = request.form.get('description')
        prerequisites = request.form.get('prerequisites')
        available_seats = int(request.form.get('seats'))

        # Save the course to the database or any other storage
        #  Execute the necessary SQL statement to insert the course data
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO courses (name, description, prerequisites, available_seats) VALUES (?, ?, ?, ?)",
                           (course_name, description, prerequisites, available_seats))
            conn.commit()

        return redirect('/courses')
    else:
        return render_template('create_course.html')

@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    if request.method == 'POST':
        course_name = request.form.get('name')
        description = request.form.get('description')
        prerequisites = request.form.get('prerequisites')
        available_seats = int(request.form.get('seats'))

        # Update the course in the database or any other storage
        # Execute the necessary SQL statement to update the course data
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE courses SET name = ?, description = ?, prerequisites = ?, available_seats = ? WHERE id = ?",
                           (course_name, description, prerequisites, available_seats, course_id))
            conn.commit()

        return redirect('/courses')
    else:
        # Retrieve the course data from the database or any other storage based on the course_id
        # Execute the necessary SQL statement to retrieve the course data
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
            course = cursor.fetchone()

        return render_template('edit_course.html', course=course)

@app.route('/enrollment')
def enrollment():
    # Retrieve available courses and student data from the database or any other source
    courses = [
        {'name': 'Course 1', 'description': 'Description 1', 'prerequisites': 'Prerequisites 1', 'available_seats': 20},
        {'name': 'Course 2', 'description': 'Description 2', 'prerequisites': 'Prerequisites 2', 'available_seats': 15},
        {'name': 'Course 3', 'description': 'Description 3', 'prerequisites': 'Prerequisites 3', 'available_seats': 10},
    ]
    students = [
        {'name': 'Student 1', 'id': '12345'},
        {'name': 'Student 2', 'id': '67890'},
        {'name': 'Student 3', 'id': '54321'},
    ]
    return render_template('enrollment.html', courses=courses, students=students)

@app.route('/enrollment_status', methods=['POST'])
def enrollment_status():
    # Process the enrollment request and save the enrollment status to the database or any other storage
    enrollment_status = 'Enrollment Successful'  # Example enrollment status message

    return render_template('enrollment_status.html', enrollment_status=enrollment_status)

@app.route('/analytics')
def analytics():
    # Retrieve analytics data from the database or any other source
    analytics_data = {'enrollment_count': 100, 'course_count': 10, 'student_count': 50}  # Example analytics data

    return render_template('analytics.html', analytics_data=analytics_data)
@app.route('/enrollment_report')
def enrollment_report():
    # Retrieve enrollment report data from the database 
    enrollment_report_data = [
        {'student_name': 'Student 1', 'course_name': 'Course 1', 'status': 'Enrolled'},
        {'student_name': 'Student 2', 'course_name': 'Course 2', 'status': 'Enrolled'},
        {'student_name': 'Student 3', 'course_name': 'Course 3', 'status': 'Enrolled'},
    ]  # Example enrollment report data

    return render_template('enrollment_report.html', enrollment_report_data=enrollment_report_data)

if __name__ == '__main__':
    app.run()
