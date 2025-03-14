import csv
import sqlite3

# Create the database and tables
def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")

    # Create courses table
    cursor.execute("CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, prerequisites TEXT, available_seats INTEGER)")

    # Create registration table
    cursor.execute("CREATE TABLE IF NOT EXISTS registration (id INTEGER PRIMARY KEY AUTOINCREMENT, gender TEXT, nationality TEXT, place_of_birth TEXT, stage_id TEXT, grade_id TEXT, section_id TEXT, topic TEXT, semester TEXT, relation TEXT, raised_hands INTEGER, visited_resources INTEGER, announcements_view INTEGER, discussion INTEGER, parent_answering_survey TEXT, parent_school_satisfaction TEXT, student_absence_days INTEGER, class_label TEXT)")

    # Create other tables
    # cursor.execute("CREATE TABLE IF NOT EXISTS enrollment (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, course_id INTEGER, status TEXT)")

    conn.commit()
    conn.close()

# Authenticate user
def authenticate_user(username, password):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            return True
        else:
            return False

# Create new user
def create_user(username, password):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return False
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True

# Save registration data
def save_registration_data(gender, nationality, place_of_birth, stage_id, grade_id, section_id, topic, semester,
                           relation, raised_hands, visited_resources, announcements_view, discussion,
                           parent_answering_survey, parent_school_satisfaction, student_absence_days, class_label):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO registration (gender, nationality, place_of_birth, stage_id, grade_id, section_id, topic, semester, relation, raised_hands, visited_resources, announcements_view, discussion, parent_answering_survey, parent_school_satisfaction, student_absence_days, class_label) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (gender, nationality, place_of_birth, stage_id, grade_id, section_id, topic, semester,
                        relation, raised_hands, visited_resources, announcements_view, discussion,
                        parent_answering_survey, parent_school_satisfaction, student_absence_days, class_label))
        conn.commit()

# Retrieve data from registration table and apply filtering logic
def retrieve_data(range_start, range_end):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registration")
        data = cursor.fetchall()

    filtered_data = []
    for row in data:
        grade_id = row[5]
        if grade_id.startswith('G-'):
            grade_id = grade_id[2:]
        try:
            grade_id = int(grade_id)
            if range_start <= grade_id <= range_end:
                filtered_data.append(row)
        except ValueError:
            continue

    return filtered_data

# Other database-related functions...

if __name__ == '__main__':
    create_database()
