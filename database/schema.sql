CREATE TABLE users (
	id INTEGER PRIMARY KEY, 
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
	id INTEGER PRIMARY KEY, 
    user_id INTEGER,
    name TEXT NOT NULL, 
    description TEXT, 
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    time_limit DATETIME,
    status BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
