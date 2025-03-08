import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1100",
    database="ResumeShortlisting"
)

print("Connected to MySQL!")
conn.close()
