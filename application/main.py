from fastapi import FastAPI, HTTPException
from functions import *
from schemes import *

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/users", response_model=OutputUser)
def create_u(user: CreateUser):
    """Создать пользователя"""
    u = create_user(user.name, user.username, user.password)
    return OutputUser(
        id=u[0],
        name=u[1],
        username=u[2],
        password=u[3],
        created_time=u[4]
    )

@app.get("/users/{identificate}", response_model=OutputUser)
def get_username(identificate):
    """Информация о пользователе по username или по id"""
    if identificate.isdigit():
        user = get_user_id(identificate)
    else:
        user = get_user_username(identificate)
    return OutputUser(
        id=user[0],
        name=user[1],
        username=user[2],
        password=user[3],
        created_time=user[4]
    )

@app.get("/users/{name}/", response_model=list[OutputUser])
def get_name(name: str):
    """Информация о пользователях по name"""
    users = get_user_name(name)
    result = [
        OutputUser(id = user[0],
                   name=user[1],
                   username=user[2],
                   password=user[3],
                   created_time=user[4])
        for user in users
    ]
    return result

@app.get("/users", response_model=list[OutputUser])
def get_all():
    """Информация о всех пользователях"""
    users = get_all_users_v2()
    result = [
        OutputUser(id=user[0],
                   name=user[1],
                   username=user[2],
                   password=user[3],
                   created_time=user[4])
        for user in users
    ]
    return result

@app.delete("/users/{username}")
def delete_u(username: str):
    """Удалить пользователя"""
    delete_user(username)
    return {"message": f"User {username} deleted"}

@app.put("/users/{user.id}", response_model=OutputUser)
def update_u(user: UpdateUser):
    """Обновить данные пользователя"""
    u = update_user(user.id, user.name, user.username, user.password)
    return OutputUser(
        id=u[0],
        name=u[1],
        username=u[2],
        password=u[3],
        created_time=u[4]
    )

@app.post("/tasks", response_model=OutputTask)
def create_t(task: CreateTask):
    '''Создание задачи'''
    task = create_task(task.user_id, task.name, task.description, task.status, task.limit_time)
    return OutputTask(id=task[0],
                   user_id=task[1],
                   name=task[2],
                   description=task[3],
                   status=task[4],
                   limit_time=task[5],
                   created_time=task[6])

@app.get("/tasks/{user_id}", response_model=list[OutputTask])
def get_all_tasks(user_id: int):
    '''Получить все задачи пользователя'''
    tasks = get_tasks(user_id)
    if not tasks:
        return []
    result = [
        OutputTask(id=task[0],
                    user_id=task[1],
                    name=task[2],
                    description=task[3],
                    status=task[4],
                    limit_time=task[5],
                    created_time=task[6])
        for task in tasks
    ]
    return result

@app.get("/tasks/{user_id}/{name}", response_model=list[OutputTask])
def get_tasks_by_name(user_id: int, name: str):
    '''Получить задачу пользователя по названию'''
    tasks = get_task_name(name, user_id)
    result = [
        OutputTask(id=task[0],
                   user_id=task[1],
                   name=task[2],
                   description=task[3],
                   status=task[4],
                   limit_time=task[5],
                   created_time=task[6])
        for task in tasks
    ]
    return result

@app.put("/tasks/{task.user_id}/{task.id}", response_model=OutputTask)
def update_t(task: UpdateTask):
    """Обновить данные о задаче"""
    t = update_task(task.id, task.user_id, task.name, task.description, task.status, task.limit_time)
    return OutputTask(id=t[0],
                      user_id=t[1],
                      name=t[2],
                      description=t[3],
                      status=t[4],
                      limit_time=t[5],
                      created_time=t[6])

@app.delete("/tasks/{user_id}/{id}")
def delete_tasks(id: int,user_id: int):
    '''Удаление задачи пользователя'''
    delete_task(id,user_id)
    return {'message': 'Задача удалена'}
