import sqlite3

conn = sqlite3.connect("app/db/sqlite.db")

cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM analysis_requests"
)

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()