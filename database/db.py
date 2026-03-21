import sqlite3

con = sqlite3.connect('task_m.db')
cur = con.cursor()

cur.execute(
    """CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT UNIQUE NOT NULL 
    );
    
    CREATE TABLE IF NOT EXISTS tasks (
    user_id INTEGER NOT NULL
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
    );
    
    CREATE TABLE IF NOT EXISTS description_t (
    task_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    time_limit TIMESTAMP,
    status BOOLEAN DEFAULT FALSE NOT NULL   
    );
    """
)
con.commit()

con.close()