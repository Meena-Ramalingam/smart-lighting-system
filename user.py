import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("user_database.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the 'user_data' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_code TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        usertype TEXT CHECK(usertype IN ('admin', 'lineman')) NOT NULL
    )
''')

# Commit the changes and close the database connection
conn.commit()
conn.close()
