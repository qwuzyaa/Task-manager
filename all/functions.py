import sqlite3
from datetime import datetime


#Для таблицы USERS
#Добавление пользователя
def create_user(name, username, password):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    cur.execute('''INSERT INTO users (name, username, password, created_time) 
    VALUES (?, ?, ?, ?)''', (name, username, password, datetime.now()))
    print (f"Пользователь {username} успешно создан!")
    con.commit()
    con.close()

#Информация об одном пользователе по username
def get_user_username(username):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM users WHERE username = ?''', (username,))
    result = cur.fetchone()
    print(result)

#Информация о пользователях по имени
def get_user_name(name):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM users WHERE name = ?''', (name,))
    result = cur.fetchall()
    for user in result:
        print(user)

#Информация о всех пользователях
def get_all_users():
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
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

#Обновление информации пользователя полностью
def update_user(id, name = None, username = None, password = None):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
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
        con.close()
        print("Пользователь обновлен!")

#Обновление имени
def update_name(id, name):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    cur.execute('''UPDATE users SET name = ? WHERE id = ?''', (name,id))
    con.commit()
    con.close()
    print("Имя пользователя обновлено!")

#Обновление username
def update_username(id, username):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    cur.execute('''UPDATE users SET username = ? WHERE id = ?''', (username, id))
    con.commit()
    con.close()
    print("Username пользователя обновлен!")

#Обновление username
def update_password(id, password):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    pas = cur.execute('''SELECT password FROM users WHERE id = ?''', (id,)).fetchone()[0]
    old_pas = int(input('Введите старый пароль: '))
    if old_pas == pas:
        cur.execute('''UPDATE users SET password = ? WHERE id = ?''', (password, id))
        con.commit()
        con.close()
        print("Пароль пользователя обновлен!")
    else:
        print('Старый пароль неправильный')

#Удаление пользователя
def delete_user(username):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    user_id = cur.execute('''SELECT id FROM users WHERE username = ?''', (username,)).fetchone()[0]
    cur.execute('''DELETE FROM users WHERE id = ?''', (user_id,))
    print (f"Пользователь {username} успешно удален!")
    con.commit()
    con.close()


#Для таблицы TASKS
#Добавление записи
def create_task(user_id, name, description, status, limit_time):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    cur.execute('''INSERT INTO tasks (user_id, name, description, status, limit_time, created_time) 
    VALUES (?, ?, ?, ?)''', (user_id, name, description, status, limit_time, datetime.now()))
    print (f"Задание '{name}' успешно добавлено!")
    con.commit()
    con.close()

#Получение списка всех задач для пользователя
def get_tasks(user_id):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM tasks WHERE user_id = ?''', (user_id,))
    result = cur.fetchall()
    for task in result:
        print(task)

#Получить задачи пользователя по названию
def get_task_name(name, user_id):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND name = ?''', (user_id, name))
    result = cur.fetchall()
    for task in result:
        print(task)

#Обновление задачи полностью
def update_task(id, name, description, status, limit_time):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    update = []
    params = []
    if name:
        update.append('name = ?')
        params.append(name)
    if description:
        update.append('description = ?')
        params.append(description)
    if status:
        update.append('status = ?')
        params.append(status)
    if limit_time:
        update.append('limit_time = ?')
        params.append(limit_time)
    if update:
        params.append(id)
        cur.execute(f'''UPDATE users SET {','.join(update)} WHERE id = ?''', params)
        con.commit()
        con.close()
        print("Задача обновлена!")

#Обновление названия задачи
def update_name_task(id, name):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    cur.execute('''UPDATE tasks SET name = ? WHERE id = ?''', (name, id))
    con.commit()
    con.close()
    print("Название обновлено")

#Обновление описания задачи
def update_name_task(id, description):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    cur.execute('''UPDATE tasks SET description = ? WHERE id = ?''', (description, id))
    con.commit()
    con.close()
    print("Описание обновлено")

#Обновление дедлайна задачи
def update_status(id, limit_time):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    cur.execute('''UPDATE tasks SET limit_time = ? WHERE id = ?''', (limit_time, id))
    con.commit()
    con.close()
    print("Дедлайн обновлен")

#Обновление статуса задачи
def update_status(id, status):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    cur.execute('''UPDATE tasks SET status = ? WHERE id = ?''', (status, id))
    con.commit()
    con.close()
    print("Статус обновлен")

#Удаление задачи
def delete_task(id):
    con = sqlite3.connect('database/task_m.db')
    cur = con.cursor()
    cur.execute('''DELETE FROM tasks WHERE id = ?''', (id,))
    con.commit()
    con.close()
    print("Задача удалена!")
