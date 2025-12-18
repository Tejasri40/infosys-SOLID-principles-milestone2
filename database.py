import sqlite3

DB_NAME = "users.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def initialize_db():
    conn = get_connection()
    cur = conn.cursor()

    # Create user table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)

    # Insert a default user only if table is empty
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]

    if count == 0:
        cur.execute("INSERT INTO users(username, password) VALUES (?, ?)", 
                    ("admin", "admin123"))
        print("Default user created: admin / admin123")

    conn.commit()
    conn.close()
