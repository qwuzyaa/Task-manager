from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateUser(BaseModel):
    name: str
    username: str
    password: int

class LoginUser(BaseModel):
    username: str
    password: int

class UpdateUser(BaseModel):
    id: int
    name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[int] = None

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

class UpdateTask(BaseModel):
    id: int
    user_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None
    limit_time: Optional[str] = None

class OutputTask(BaseModel):
    id: int
    user_id: int
    name: str
    description: str
    status: int
    limit_time: str
    created_time: str
