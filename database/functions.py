import sqlite3
from datetime import datetime

con = sqlite3.connect('task_m.db')
cur = con.cursor()

# Для таблицы USERS
# Добавление пользователя
def create_user(name, username, password):
    cur.execute('''INSERT INTO users (name, username, password, created_time) 
    VALUES (?, ?, ?, ?)''', (name, username, password, datetime.now()))
    print (f"Пользователь {username} успешно создан!")
    con.commit()

#Удаление пользователя
def delete_user(username):
    user_id = cur.execute('''SELECT id FROM users WHERE username = ?''', (username,)).fetchone()[0]
    cur.execute('''DELETE FROM users WHERE id = ?''', (user_id,))
    print (f"Пользователь {username} успешно удален!")
    con.commit()

#Обновление информации пользователя  


# Добавление записи
def create_task(user_id, name, description, status, limit_time):
    cur.execute('''INSERT INTO tasks (user_id, name, description, status, limit_time, created_time) 
    VALUES (?, ?, ?, ?)''', (user_id, name, description, status, limit_time, datetime.now()))
    print (f"Задание '{name}' успешно добавлено!")
    con.commit()



