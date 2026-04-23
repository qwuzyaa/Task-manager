from fastapi import FastAPI, HTTPException, Header, Depends, status
from functions import *
from schemes import *
import uvicorn

app = FastAPI()

admin_key = 'Task-manager-admin'

'''
def get_current_user_id(x_user_id: int = Header(..., alias="X-User-Id")) -> int:
    """Получает текущего пользователя из заголовка"""
    user = get_user_id(x_user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return x_user_id
'''

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/register", tags = ['User'], response_model=OutputUser, status_code=status.HTTP_201_CREATED)
def register_user(user: CreateUser):
    """Регистрация пользователя"""
    trying = get_user_username(user.username)
    if trying:
        raise HTTPException(status_code=400, detail="User already exists")

    user_id = create_user(user.name, user.username, user.password)
    if user_id is None:
        raise HTTPException(status_code=500, detail="Failed to create user")

    u = get_user_id(user_id)
    if u is None:
        raise HTTPException(status_code=500, detail="User not found but created")

    return OutputUser(
        id=u[0],
        name=u[1],
        username=u[2],
        created_time=u[3]
    )

@app.post("/login", tags = ['User'], status_code=status.HTTP_200_OK)
def login_user(user: LoginUser):
    """Вход пользователя"""
    u = get_user_username(user.username)
    if u is None or int(u[3]) != user.password:
        raise HTTPException(status_code=401, detail="Invalid data")
    return {
        "message": "Login successful",
        "user_id": u[0],
        "username": u[2]
    }

@app.get("/users/{identificate}", tags = ['User'], response_model=OutputUser, status_code=status.HTTP_200_OK)
def get_by_id(identificate):
    """Информация о пользователе по username или по id"""
    if identificate.isdigit():
        user = get_user_id(identificate)
    else:
        user = get_user_username(identificate)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return OutputUser(
        id=user[0],
        name=user[1],
        username=user[2],
        created_time=user[3]
    )

'''
@app.get("/users/{name}/", tags = ['User'], response_model=list[OutputUser], status_code=status.HTTP_200_OK)
def get_name(name: str):
    """Информация о пользователях по name"""
    users = get_user_name(name)
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    result = [
        OutputUser(id = user[0],
                   name=user[1],
                   username=user[2],
                   created_time=user[3])
        for user in users
    ]
    return result
'''

@app.get("/admin/users", tags = ['User'], status_code=status.HTTP_200_OK)
def get_all(key: str):
    """Информация о всех пользователях"""
    if key != admin_key:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    else:
        users = get_all_users_v2()
        if len(users)==0:
            return {'message': 'No users exist'}
        else:
            result = [
                OutputUser(id=user[0],
                           name=user[1],
                           username=user[2],
                           created_time=user[3])
                for user in users
            ]
            return result

@app.delete("/users/{username}",tags = ['User'], status_code=status.HTTP_200_OK)
def delete_u(username: str):
    """Удалить пользователя"""
    users = get_user_username(username)
    if users is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        delete_user(username)
        u = get_user_username(username)
        if len(u) != 0:
            raise HTTPException(status_code=500, detail="Cannot delete user")
        else:
            return {"message": f"User {username} deleted"}


@app.put("/users/{user.id}", tags = ['User'], response_model=OutputUser)
def update_u(user: UpdateUser):
    """Обновить данные пользователя"""
    u = update_user(user.id, user.name, user.username, user.password)
    return OutputUser(
        id=u[0],
        name=u[1],
        username=u[2],
        created_time=u[3]
    )

@app.post("/tasks", tags = ['Task'], response_model=OutputTask, status_code=status.HTTP_201_CREATED)
def create_t(task: CreateTask):
    """Создание задачи"""
    task = create_task(task.user_id, task.name, task.description, task.status, task.limit_time)
    return OutputTask(id=task[0],
                   user_id=task[1],
                   name=task[2],
                   description=task[3],
                   status=task[4],
                   limit_time=task[5],
                   created_time=task[6])

@app.get("/tasks/{user_id}", tags = ['Task'], response_model=list[OutputTask], status_code=status.HTTP_200_OK)
def get_all_tasks(user_id: int):
    """Получить все задачи пользователя"""
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

@app.get("/tasks/{user_id}/{name}", tags = ['Task'], response_model=list[OutputTask], status_code=status.HTTP_200_OK)
def get_tasks_by_name(user_id: int, name: str):
    """Получить задачу пользователя по названию"""
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

@app.put("/tasks/{task.user_id}/{task.id}", tags = ['Task'], response_model=OutputTask)
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

@app.delete("/tasks/{user_id}/{id}", tags = ['Task'], status_code=status.HTTP_204_NO_CONTENT)
def delete_tasks(id: int,user_id: int):
    """Удаление задачи пользователя"""
    delete_task(id,user_id)
    #return {'message': 'Задача удалена'}

'''
if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)
'''