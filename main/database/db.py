import sqlite3

con = sqlite3.connect('task_m.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT UNIQUE NOT NULL,
    created_time TEXT NOT NULL
);
'''
)

cur.execute('''CREATE TABLE IF NOT EXISTS tasks (
    user_id INTEGER NOT NULL,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    status INTEGER DEFAULT 0, 
    limit_time TEXT,
    created_time TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
'''
)

con.commit()
con.close()