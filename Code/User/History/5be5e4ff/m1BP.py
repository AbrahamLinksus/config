import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="test_db"
)

print("Connected to MySQL!")
conn.close()
