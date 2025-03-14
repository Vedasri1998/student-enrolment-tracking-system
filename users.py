import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Fetch all the user credentials from the database
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

# Display the credentials
for user in users:
    print(f"User: {user}")

# Close the database connection
conn.close()
