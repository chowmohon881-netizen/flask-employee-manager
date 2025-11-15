import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("SELECT id, username, password FROM users")
rows = cursor.fetchall()
conn.close()

print(rows)
