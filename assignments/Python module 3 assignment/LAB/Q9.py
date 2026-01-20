#Connect to SQLite3, create table, insert & fetch data
import sqlite3

conn = sqlite3.connect("student.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS student(id INTEGER, name TEXT)")
cursor.execute("INSERT INTO student VALUES (1, 'Hiren')")

cursor.execute("SELECT * FROM student")
print(cursor.fetchall())

conn.commit()
conn.close()
