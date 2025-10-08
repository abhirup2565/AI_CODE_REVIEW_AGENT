import psycopg2

conn = psycopg2.connect(
    dbname="ai_review_db",
    user="ai_user",
    password="ai_pass",
    host="127.0.0.1",
    port=5433
)
print("Connected!")
conn.close()
