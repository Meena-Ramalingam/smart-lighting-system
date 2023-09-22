import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("smart_lighting_system.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the 'smart_lighting_data' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS smart_lighting_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pole_no TEXT NOT NULL,
        area TEXT NOT NULL,
        time TEXT NOT NULL,
        date TEXT NOT NULL,
        error_code TEXT NOT NULL,
        error_type TEXT NOT NULL,
      
        is_pending BOOLEAN NOT NULL
    )
''')

# Commit the changes and close the database connection
conn.commit()
conn.close()
