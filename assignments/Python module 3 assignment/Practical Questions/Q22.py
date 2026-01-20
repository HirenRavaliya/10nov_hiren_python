# Practical Question 22: Insert data and fetch from SQLite3 database
import sqlite3

conn = sqlite3.connect("test.db")
cur = conn.cursor()
cur.execute("INSERT INTO user VALUES (1, 'Hiren')")
cur.execute("SELECT * FROM user")
print(cur.fetchall())
conn.commit()
conn.close()
