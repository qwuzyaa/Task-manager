CREATE TABLE users (
	id INTEGER PRIMARY KEY, 
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
	id INTEGER PRIMARY KEY, 
    user_id INTEGER,
    name VARCHAR(255) NOT NULL, 
    description VARCHAR(255), 
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    time_limit DATETIME,
    status BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id)
);