import sqlite3

conn = sqlite3.connect("complaints.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
mobile TEXT,
email TEXT,
category TEXT,
priority TEXT,
location TEXT,
image TEXT,
status TEXT DEFAULT 'Pending',
feedback TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
mobile TEXT,
role TEXT DEFAULT 'user'
)
""")

conn.commit()
conn.close()
print("Database Created Successfully")