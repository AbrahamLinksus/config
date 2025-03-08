
import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1100",
    database="ResumeShortlisting",
    charset="utf8mb4",
    collation="utf8mb4_general_ci"
)
print("Connected to MySQL")
conn.close()

