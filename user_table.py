import sqlite3
conn = sqlite3.connect("db/userdb.db", check_same_thread=False)

def create_table():
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY autoincrement,
        username text,
        email text,
        password text)
        """)
    conn.commit()