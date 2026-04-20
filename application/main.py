from fastapi import FastAPI, HTTPException
from functions import *

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/users/{username}")
def get_username(username: str):
    """Информация о пользователе по username"""
    user = get_user_username(username)
    return user

@app.get("/users/{name}/")
def get_name(name: str):
    """Информация о пользователях по name"""
    user = get_user_name(name)
    return user

@app.get("/users")
def get_all():
    """Информация о всех пользователях"""
    users = get_all_users_v2()
    return users

@app.post("/users")
def create_u(name: str, username: str, password: str):
    """Создать пользователя"""
    create_user(name, username, password)
    return f"Пользователь {username} успешно создан!"

@app.delete("/users/{username}")
def delete_u(username: str):
    """Удалить пользователя"""
    delete_user(username)

@app.put("/users/{id}")
def update_u(id: int, name: str, username: str, password: str):
    """Обновить данные пользователя"""
    if name == username == password == None:
        return "Данные прежние"
    else:
        update_user(id, name, username, password)
        return "Пользователь обновлен"

@app.post("/tasks")
def create_t(user_id: int, name: str, description: str, status: int, limit_time: str):
    '''Создание задачи'''
    task = create_task(user_id, name, description, status, limit_time)
    return task

@app.put("/tasks/{id}")
def update_t(id: int, name: str, description: str, status: int, limit_time: str):
    """Обновить данные о задаче"""
    if name == description == status == limit_time == None:
        return "Данные прежние"
    else:
        update_task(id, name, description, status, limit_time)
        return "Задача обновлена"

@app.get("/tasks/{user_id}")
def get_all_tasks(user_id):
    '''Получить все задачи пользователя'''
    tasks = get_tasks(user_id)
    return tasks

@app.get("tasks/{user_id}")
def get_tasks(name, user_id):
    '''Получить задачу пользователя по названию'''
    tasks = get_task_name(name, user_id)
    return tasks

@app.delete("/tasks/{user_id}/{id}")
def delete_tasks(id,user_id):
    '''Удаление задачи пользователя'''
    delete_task(id,user_id)
    return {'message': 'Задача удалена'}
