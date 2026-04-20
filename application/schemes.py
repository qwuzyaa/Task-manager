from pydantic import BaseModel
from datetime import datetime

class CreateUser(BaseModel):
    name: str
    username: str
    password: int

class OutputUser(BaseModel):
    id: int
    name: str
    username: str
    password: int
    created_time: str

class CreateTask(BaseModel):
    user_id: int
    name: str
    description: str
    status: int
    limit_time: str

class OutputTask(BaseModel):
    id: int
    user_id: int
    name: str
    description: str
    status: int
    limit_time: str
    created_time: str
