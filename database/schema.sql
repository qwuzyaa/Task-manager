CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT UNIQUE NOT NULL,
    created_time TEXT NOT NULL
);

CREATE TABLE tasks (
	user_id INTEGER NOT NULL,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    status INTEGER DEFAULT 0, 
    limit_time TEXT,
    created_time TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
