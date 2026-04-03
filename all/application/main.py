from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
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
    user = create_user(name, username, password)
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

