import sqlite3
from datetime import datetime

DB_PATH = r"C:\Users\User\Task-manager\database\task_m.db"

#Для таблицы USERS
#Добавление пользователя
def create_user(name, username, password):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''INSERT INTO users (name, username, password, created_time) 
    VALUES (?, ?, ?, ?)''', (name, username, password, datetime.now()))
    user = cur.execute('''SELECT id FROM users WHERE username = ?''', (username,)).fetchone()[0]
    con.commit()
    con.close()
    return user

#Информация об одном пользователе по username
def get_user_username(username):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT id, name, username, created_time FROM users WHERE username = ?''', (username,))
    result = cur.fetchone()
    con.close()
    return result

#Информация о пользователях по имени
def get_user_name(name):
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute('''SELECT id, name, username, created_time FROM users WHERE name = ?''', (name,))
        result = cur.fetchall()
        con.close()
        return result
    except sqlite3.OperationalError as e:
        return e
#Информация о пользователях по id
def get_user_id(id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT id, name, username, created_time FROM users WHERE id = ?''', (id,))
    result = cur.fetchone()
    con.close()
    return result

def get_all_users_v2():
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute('''SELECT id, name, username, created_time FROM users''')
        result = cur.fetchall()
        con.close()
        return result
    except sqlite3.OperationalError as e:
        raise e
    except Exception as e:
        raise e
#Обновление информации пользователя полностью
def update_user(id, name = None, username = None, password = None):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    update = []
    params = []
    if name is not None:
        update.append ('name = ?')
        params.append (name)
    if username is not None:
        update.append ('username = ?')
        params.append (username)
    if password is not None:
        update.append('password = ?')
        params.append(password)

    if len(update)>0:
        params.append(id)
        cur.execute(f'''UPDATE users SET {','.join(update)} WHERE id = ?''', params )
        user = cur.execute('''SELECT id, name, username, created_time FROM users WHERE id = ?''', (id,)).fetchone()
        con.commit()
    else:
        user = cur.execute('''SELECT id, name, username, created_time FROM users WHERE id = ?''', (id,)).fetchone()
        con.commit()
    con.close()
    return user
    #else:
        #user = cur.execute('''SELECT * FROM users WHERE id = ?''', (id,)).fetchone()
        #return "Данные не обновлялись"

#Обновление имени
def update_name(id, name):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    result = cur.execute('''UPDATE users SET name = ? WHERE id = ?''', (name,id))
    con.commit()
    con.close()
    return result

#Обновление username
def update_username(id, username):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    result = cur.execute('''UPDATE users SET username = ? WHERE id = ?''', (username, id))
    con.commit()
    con.close()
    return result

#Обновление username
def update_password_v1(id, password):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    pas = cur.execute('''SELECT password FROM users WHERE id = ?''', (id,)).fetchone()[0]
    old_pas = int(input('Введите старый пароль: '))
    if old_pas == pas:
        cur.execute('''UPDATE users SET password = ? WHERE id = ?''', (password, id))
        con.commit()
        con.close()
        #return "Пароль пользователя обновлен!"
    else:
        return 'Старый пароль неправильный'

def update_password_v2(id, password):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    pas = cur.execute('''SELECT password FROM users WHERE id = ?''', (id,)).fetchone()[0]
    result = cur.execute('''UPDATE users SET password = ? WHERE id = ?''', (password, id))
    con.commit()
    con.close()
    return result

#Удаление пользователя
def delete_user(username):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    user_id = cur.execute('''SELECT id FROM users WHERE username = ?''', (username,)).fetchone()[0]
    cur.execute('''DELETE FROM users WHERE id = ?''', (user_id,))
    con.commit()
    con.close()
    #return f"Пользователь {username} успешно удален!"

def delete_user_id(id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''DELETE FROM users WHERE id = ?''', (id,))
    con.commit()
    con.close()

#Для таблицы TASKS
#Добавление записи
def create_task(user_id, name, description, status, limit_time):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''INSERT INTO tasks (user_id, name, description, status, limit_time, created_time) 
    VALUES (?, ?, ?, ?, ?, ?)''', (user_id, name, description, status, limit_time, datetime.now()))
    task = cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND id = ?''', (user_id, cur.lastrowid)).fetchone()
    con.commit()
    con.close()
    return task

#Получение списка всех задач для пользователя
def get_tasks(user_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT * FROM tasks WHERE user_id = ?''', (user_id,))
    result = cur.fetchall()
    con.close()
    return result

#Получить задачи пользователя по названию
def get_task_name(name, user_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND name = ?''', (user_id, name))
    result = cur.fetchall()
    con.close()

    return result

#Обновление задачи полностью
def update_task(id, user_id, name, description, status, limit_time):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    update = []
    params = []
    if name is not None:
        update.append('name = ?')
        params.append(name)
    if description is not None:
        update.append('description = ?')
        params.append(description)
    if status is not None:
        update.append('status = ?')
        params.append(status)
    if limit_time is not None:
        update.append('limit_time = ?')
        params.append(limit_time)
    if len(update)>0:
        params.append(id)
        cur.execute(f'''UPDATE tasks SET {','.join(update)} WHERE id = ?''', params)
        task = cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND id = ?''', (user_id, id)).fetchone()
        con.commit()
    else:
        task = cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND id = ?''', (user_id, id)).fetchone()
        con.commit()
    con.close()
    return task

#Обновление названия задачи
def update_name_task(id, name):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''UPDATE tasks SET name = ? WHERE id = ?''', (name, id))
    con.commit()
    con.close()
    print("Название обновлено")

#Обновление описания задачи
def update_name_task(id, description):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''UPDATE tasks SET description = ? WHERE id = ?''', (description, id))
    con.commit()
    con.close()
    print("Описание обновлено")

#Обновление дедлайна задачи
def update_status(id, limit_time):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''UPDATE tasks SET limit_time = ? WHERE id = ?''', (limit_time, id))
    con.commit()
    con.close()
    print("Дедлайн обновлен")

#Обновление статуса задачи
def update_status(id, status):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''UPDATE tasks SET status = ? WHERE id = ?''', (status, id))
    con.commit()
    con.close()
    print("Статус обновлен")

#Удаление задачи
def delete_task(id, user_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''DELETE FROM tasks WHERE id = ? AND user_id = ?''', (id,user_id))
    con.commit()
    con.close()
    #print("Задача удалена!")
