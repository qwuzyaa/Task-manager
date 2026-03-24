import sqlite3
from datetime import datetime

con = sqlite3.connect('task_m.db')
cur = con.cursor()

#Для таблицы USERS
#Добавление пользователя
def create_user(name, username, password):
    cur.execute('''INSERT INTO users (name, username, password, created_time) 
    VALUES (?, ?, ?, ?)''', (name, username, password, datetime.now()))
    print (f"Пользователь {username} успешно создан!")
    con.commit()

#Информация об одном пользователе по username
def get_user_username(username):
    cur.execute('''SELECT * FROM users WHERE username = ?''', (username,))
    result = cur.fetchone()
    print(result)

#Информация о пользователях по имени
def get_user_name(name):
    cur.execute('''SELECT * FROM users WHERE name = ?''', (name,))
    result = cur.fetchall()
    for user in result:
        print(user)

#Информация о всех пользователях
def get_all_users():
    admin = int(input('Введите пароль: '))
    if admin == 123456789:
        cur.execute('''SELECT * FROM users''')
        result = cur.fetchall()
        for user in result:
            print(user)
    else:
        cur.execute('''SELECT name, username FROM users''')
        result = cur.fetchall()
        for user in result:
            print(user)

#Обновление информации пользователя
def update_user(id, name = None, username = None, password = None):
    update = []
    params = []

    if name:
        update.append ('name = ?')
        params.append (name)
    if username:
        update.append ('username = ?')
        params.append (username)
    if password:
        pas = cur.execute('''SELECT password FROM users WHERE id = ?''', (id,)).fetchone()[0]
        old_pas = int(input('Введите старый пароль: '))
        if old_pas == pas:
            update.append('password = ?')
            params.append (password)
        else:
            print('Старый пароль неправильный')
    if update:
        params.append(id)
        cur.execute(f'''UPDATE users SET {','.join(update)} WHERE id = ?''', params )
        con.commit()
        print("Пользователь обновлен!")

#Удаление пользователя
def delete_user(username):
    user_id = cur.execute('''SELECT id FROM users WHERE username = ?''', (username,)).fetchone()[0]
    cur.execute('''DELETE FROM users WHERE id = ?''', (user_id,))
    print (f"Пользователь {username} успешно удален!")
    con.commit()


#Для таблицы TASKS
#Добавление записи
def create_task(user_id, name, description, status, limit_time):
    cur.execute('''INSERT INTO tasks (user_id, name, description, status, limit_time, created_time) 
    VALUES (?, ?, ?, ?)''', (user_id, name, description, status, limit_time, datetime.now()))
    print (f"Задание '{name}' успешно добавлено!")
    con.commit()

#Получение списка всех задач для пользователя
def get_tasks(user_id):
    cur.execute('''SELECT * FROM tasks WHERE user_id = ?''', (user_id,))
    result = cur.fetchall()
    for task in result:
        print(task)



