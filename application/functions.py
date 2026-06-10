import sqlite3
from datetime import datetime
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(current_dir, "database", "task_m.db")

"""Пользователь"""
#Добавление пользователя
def create_user(name, username, password):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''INSERT INTO users (name, username, password, created_time) VALUES (?, ?, ?, ?)''', (name, username, password, datetime.now()))
    user_id = cur.lastrowid
    con.commit()
    con.close()
    return user_id

#Проверка пароля
def check_login(username, password):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('SELECT id, password FROM users WHERE username = ? AND password = ?', (username, password))
    result = cur.fetchone()
    con.close()
    return result

#Информация об одном пользователе по username
def get_user_username(username):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT id, name, username, created_time FROM users WHERE username = ?''', (username,))
    result = cur.fetchone()
    con.close()
    return result

#Получение пароля username
def get_pass(username):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT password FROM users WHERE username = ?''', (username,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    return None

#Получение пароля id
def get_pass_id(id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT password FROM users WHERE usernameid = ?''', (id,))
    result = cur.fetchone()
    con.close()
    if result:
        return result[0]
    return None

#Получение id
def get_id(username, password):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT id FROM users WHERE username = ? AND password = ?''', (username, password))
    result = cur.fetchone()
    con.close()
    return result

#Информация о пользователях по имени
def get_user_name(name):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT id, name, username, created_time FROM users WHERE name = ?''', (name,))
    result = cur.fetchall()
    con.close()
    return result

#Информация о пользователях по id
def get_user_id(id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT id, name, username, created_time FROM users WHERE id = ?''', (id,))
    result = cur.fetchone()
    con.close()
    return result

#Информация о всех пользователях
def get_all_users_v2():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT id, name, username, created_time FROM users''')
    result = cur.fetchall()
    con.close()
    return result

#Обновление информации пользователя полностью
def update_user(id, name, username, password):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    update = []
    params = []
    if name is not None:
        update.append('name = ?')
        params.append(name)
    if username is not None:
        update.append('username = ?')
        params.append(username)
    if password is not None:
        update.append('password = ?')
        params.append(password)

    if len(update) > 0:
        params.append(id)
        cur.execute(f'''UPDATE users SET {','.join(update)} WHERE id = ?''', params)
        user = cur.execute('''SELECT id, name, username, created_time FROM users WHERE id = ?''', (id,)).fetchone()
        con.commit()
    else:
        user = cur.execute('''SELECT id, name, username, created_time FROM users WHERE id = ?''', (id,)).fetchone()
        con.commit()
    con.close()
    return user

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
def delete_user_id(id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''DELETE FROM users WHERE id = ?''', (id,))
    con.commit()
    con.close()

"""Задачи"""
#Добавление записи
def create_task(user_id, name, description, limit_time):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    status = 0
    priority = 0
    cur.execute('''INSERT INTO tasks (user_id, name, description, status, limit_time, created_time, priority) VALUES (?, ?, ?, ?, ?, ?, ?)''', (user_id, name, description, status, limit_time, datetime.now(), priority))
    task = cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND id = ?''', (user_id, cur.lastrowid)).fetchone()
    con.commit()
    con.close()
    return task

#Получение списка всех задач для пользователя
def get_tasks(user_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT * FROM tasks WHERE user_id = ? GROUP BY id ORDER BY id DESC''', (user_id,))
    result = cur.fetchall()
    con.close()
    return result

#Получить задачи пользователя по названию
def get_task_name(name, user_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM tasks WHERE user_id = ? AND name = ?", (user_id, name))
    result = cur.fetchall()
    con.close()
    return result

#Получить задачу пользователя по id
def get_task_id(id, user_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND id = ?''', (user_id, id))
    result = cur.fetchone()
    con.close()
    return result

#Обновление задачи полностью
def update_task(id, user_id, name, description, status, limit_time, priority):
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
    if limit_time is None:
        update.append('limit_time = NULL')
    elif limit_time is not None:
        update.append('limit_time = ?')
        params.append(limit_time)
    if priority is not None:
        update.append('priority = ?')
        params.append(priority)
    if len(update) > 0:
        params.append(id)
        cur.execute(f'''UPDATE tasks SET {','.join(update)} WHERE id = ?''', params)
        task = cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND id = ?''', (user_id, id)).fetchone()
        con.commit()
    else:
        task = cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND id = ?''', (user_id, id)).fetchone()
        con.commit()
    con.close()
    return task

#Обновление задачи ез статуса
def update_task_v2(id, user_id, name, description, limit_time):
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
    if limit_time is not None:
        update.append('limit_time = ?')
        params.append(limit_time)
    if len(update) > 0:
        params.append(id)
        cur.execute(f'''UPDATE tasks SET {','.join(update)} WHERE id = ?''', params)
        #task = cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND id = ?''', (user_id, id)).fetchone()
        con.commit()
    #else:
        #task = cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND id = ?''', (user_id, id)).fetchone()
        #con.commit()
    con.close()
    #return task

#Обновление названия задачи
def update_name_task(id, name):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''UPDATE tasks SET name = ? WHERE id = ?''', (name, id))
    con.commit()
    con.close()
    print("Название обновлено")

#Обновление описания задачи
def update_description_task(id, description):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''UPDATE tasks SET description = ? WHERE id = ?''', (description, id))
    con.commit()
    con.close()
    print("Описание обновлено")

#Обновление дедлайна задачи
def update_deadline(id, limit_time):
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
    #print("Статус обновлен")

#Обновление приоритета задачи
def update_priority(task_id, priority):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("UPDATE tasks SET priority = ? WHERE id = ?", (priority, task_id))
    con.commit()
    con.close()

#Удаление задачи
def delete_task(id, user_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''DELETE FROM tasks WHERE id = ? AND user_id = ?''', (id, user_id))
    con.commit()
    con.close()

"""Фильтрация"""
#Завершенные
def get_tasks_complited(user_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND status = 1''', (user_id,))
    result = cur.fetchall()
    con.close()
    return result

#В процессе
def get_tasks_active(user_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    today = datetime.now().date()
    cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND status = 0''', (user_id,))
    tasks = cur.fetchall()
    con.close()
    result = []
    for i in tasks:
        limit_time = i[5]
        if limit_time and i[4] != 1:
            deadline = datetime.strptime(limit_time, "%Y-%m-%d").date()
            if deadline >= today:
                result.append(i)
    return result

#Просроченные
def get_tasks_over(user_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    today = datetime.now().date()
    cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND status = 0 GROUP BY limit_time ORDER BY limit_time''', (user_id,))
    tasks = cur.fetchall()
    con.close()
    result = []
    for i in tasks:
        limit_time = i[5]
        if limit_time and i[4] != 1:
            deadline = datetime.strptime(limit_time, "%Y-%m-%d").date()
            if deadline < today:
                result.append(i)
    return result

#По дате окончания
def get_tasks_limit(user_id):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT * FROM tasks WHERE user_id = ? GROUP BY limit_time ORDER BY limit_time''', (user_id,))
    tasks = cur.fetchall()
    con.close()
    result = [task for task in tasks if task[5]!=None]
    return result

#Приоритеты
def get_tasks_priority(user_id, priority):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('''SELECT * FROM tasks WHERE user_id = ? AND priority = ?''', (user_id, priority))
    result = cur.fetchall()
    con.close()
    return result
