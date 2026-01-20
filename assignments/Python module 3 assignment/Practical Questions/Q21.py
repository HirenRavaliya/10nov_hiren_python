# Practical Question 21: Create a database and table using SQLite3
import sqlite3

conn = sqlite3.connect("test.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS user(id INTEGER, name TEXT)")
conn.commit()
conn.close()
