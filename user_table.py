import sqlite3

# Conecte-se ao banco de dados ou crie-o se não existir
conn = sqlite3.connect("db/userdb.db", check_same_thread=False)

def create_table():
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT)
    """)
    conn.commit()

# Chame a função create_table para criar a tabela users
create_table()
