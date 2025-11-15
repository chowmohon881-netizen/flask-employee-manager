import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

username = "mohon"
email = "mohon@example.com"
password = "abcd1234"  # the password you want to use

hashed = pwd_context.hash(password)

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
    (username, email, hashed)
)

conn.commit()
conn.close()

print("User created successfully!")
