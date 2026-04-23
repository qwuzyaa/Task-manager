from fastapi import status, HTTPException, Header, Depends, APIRouter
from application.functions import *
from application.schemes import *
import sqlite3

router = APIRouter()

admin_key = 'Task-manager-admin'

def get_current_user_id(x_user_id: int = Header(..., alias="X-User-Id")) -> int:
    """Получаем текущего пользователя из заголовка"""
    user = get_user_id(x_user_id)
    #f not user:
        #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
    return x_user_id

@router.get("/api")
def root():
    return {"message": "Hello World"}

@router.post("/api/register", tags = ['User'], response_model=OutputUser, status_code=status.HTTP_201_CREATED)
def register_user(user: CreateUser):
    """Регистрация пользователя"""
    try:
        trying = get_user_username(user.username)
        if trying:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

        user_id = create_user(user.name, user.username, user.password)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")

        u = get_user_id(user_id)
        if u is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User not found but created")

        return OutputUser(
            id=u[0],
            name=u[1],
            username=u[2],
            created_time=u[3]
            )
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/api/login", tags = ['User'], status_code=status.HTTP_200_OK)
def login_user(user: LoginUser):
    """Вход пользователя"""
    try:
        pas = get_user_pass(user.username)
        u = get_user_username(user.username)
        if pas is None and u is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No such user")
        if str(pas) != user.password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid data")
        return {
           "message": "Login successful",
           "user_id": u[0],
           "username": u[2]
        }
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/api/users/{id}", tags = ['User'], response_model=OutputUser, status_code=status.HTTP_200_OK)
def get_by_id(id: int):
    """Информация о пользователе по id"""
    try:
        user = get_user_id(id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return OutputUser(
            id=user[0],
            name=user[1],
            username=user[2],
            created_time=user[3]
        )
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/api/admin/users", tags = ['User'], status_code=status.HTTP_200_OK)
def get_all(key: str):
    """Информация о всех пользователях"""
    try:
        if key != admin_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")
        else:
            users = get_all_users_v2()
            if len(users)==0:
                raise HTTPException(status_code=status.HTTP_200_OK, detail="No users exist")
            else:
                result = [
                    OutputUser(id=user[0],
                                name=user[1],
                                username=user[2],
                                created_time=user[3])
                    for user in users
                ]
                return result
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/api/users/{id}",tags = ['User'], status_code=status.HTTP_200_OK)
def delete_u(id: int):
    """Удалить пользователя"""
    try:
        users = get_user_id(id)
        if users is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        else:
            delete_user_id(id)
            u = get_user_id(id)
            if u is not None:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Cannot delete user")
            else:
                return {"message": f"User deleted"}
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/api/users/{id}", tags = ['User'], response_model=OutputUser)
def update_u(user: UpdateUser, id: int ):
    """Обновить данные пользователя"""
    try:
        trying_1 = get_user_username(user.username)
        if trying_1 is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if user.name is None and user.username is None and user.password is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nothing to update")
        if user.username is not None:
            if trying_1 is not None and int(trying_1[0]) != id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is already in use")
            else:
                u = update_user(id, user.name, user.username, user.password)
                if u is None:
                   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
                return OutputUser(
                    id=u[0],
                    name=u[1],
                    username=u[2],
                    created_time=u[3]
                )
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/api/tasks", tags = ['Task'], response_model=OutputTask, status_code=status.HTTP_201_CREATED)
def create_t(task: CreateTask, user_id: int):
    """Создание задачи"""
    try:
        user = get_user_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such user")
        task = create_task(user_id, task.name, task.description, task.status, task.limit_time)
        if task is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Cannot create task")
        return OutputTask(
            user_id=task[0],
            id=task[1],
            name=task[2],
            description=task[3],
            status=task[4],
            limit_time=task[5],
            created_time=task[6]
        )
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/api/tasks/{user_id}", tags = ['Task'], response_model=list[OutputTask], status_code=status.HTTP_200_OK)
def get_all_tasks(user_id: int):
    """Получить все задачи пользователя"""
    try:
        user = get_user_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such user")
        tasks = get_tasks(user_id)
        if not tasks:
            raise HTTPException(status_code=status.HTTP_200_OK, detail="You do not have any tasks")
        result = [
            OutputTask(
                user_id=task[0],
                id=task[1],
                name=task[2],
                description=task[3],
                status=task[4],
                limit_time=task[5],
                created_time=task[6])
            for task in tasks
        ]
        return result
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/api/tasks/search/{name}", tags = ['Task'], response_model=list[OutputTask], status_code=status.HTTP_200_OK)
def get_tasks_by_name(name: str, user_id: int):
    """Получить задачи пользователя по названию"""
    try:
        user = get_user_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such user")
        tasks = get_task_name(name, user_id)
        if len(tasks) == 0:
            raise HTTPException(status_code=status.HTTP_200_OK, detail="There are no tasks with that name")
        result = [
            OutputTask(
                user_id=task[0],
                id=task[1],
                name=task[2],
                description=task[3],
                status=task[4],
                limit_time=task[5],
                created_time=task[6]
            )
            for task in tasks
        ]
        return result
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/api/tasks/task/{id}", tags = ['Task'], response_model=OutputTask, status_code=status.HTTP_200_OK)
def get_task_by_id(id: int, user_id: int):
    """Получить задачу пользователя по id"""
    try:
        user = get_user_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such user")
        task = get_task_id(id, user_id)
        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return OutputTask(
            user_id=task[0],
            id=task[1],
            name=task[2],
            description=task[3],
            status=task[4],
            limit_time=task[5],
            created_time=task[6]
        )
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/api/tasks/{user_id}/{id}", tags = ['Task'], response_model=OutputTask)
def update_t(id: int, task: UpdateTask, user_id: int):
    """Обновить данные о задаче"""
    try:
        trying = get_task_by_id(id, user_id)
        if trying is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        if task.name is None and task.description is None and task.status is None and task.limit_time is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nothing to update")
        t = update_task(id, user_id, task.name, task.description, task.status, task.limit_time)
        if t is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return OutputTask(
            user_id=t[0],
            id=t[1],
            name=t[2],
            description=t[3],
            status=t[4],
            limit_time=t[5],
            created_time=t[6]
        )
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/api/tasks/{user_id}/{id}", tags = ['Task'], status_code=status.HTTP_200_OK)
def delete_tasks(id: int, user_id: int):
    """Удаление задачи пользователя"""
    try:
        task = get_task_id(id, user_id)
        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        delete_task(id,user_id)
        trying = get_task_id(id, user_id)
        if trying is not None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Can't delete task")
        else:
            return {'message': 'Task was deleted'}
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
