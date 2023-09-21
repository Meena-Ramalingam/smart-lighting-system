import sqlite3

# Create a connection to the database (or create a new one if it doesn't exist)
conn = sqlite3.connect("error_db.db")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Define the table schema with "is_emergency" as INTEGER (0 or 1)
cursor.execute('''
CREATE TABLE IF NOT EXISTS errors (
    id INTEGER PRIMARY KEY,
    error_code TEXT NOT NULL,
    error_type TEXT NOT NULL
   
)
'''
)


# Commit the changes and close the connection
conn.commit()
conn.close()
