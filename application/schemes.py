from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
import re
import datetime

class CreateUser(BaseModel):
    name: str = Field(..., min_length=1, max_length=20)
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if re.search(r'[!@":;№()/|#$%^&*?]', v):
            raise ValueError('Name must not contain special characters')
        if re.search(r'[0-9]', v):
            raise ValueError('Name must not contain numbers')
        if " " in v:
            raise ValueError('Name must not contain spaces')
        return v

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if re.search(r'[!@":;№()/|#$%^&*?]', v):
            raise ValueError('Username must not contain special characters')
        if " " in v:
            raise ValueError('Username must not contain spaces')
        if not re.search(r'[a-zA-Z]', v):
            raise ValueError('Username must contain letters')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if " " in v:
            raise ValueError('Password must not contain spaces')
        if  not re.search(r'[!@#$%^&*?]', v):
            raise ValueError('Password must not contain at least one special character !@#$%^&*?')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must not contain at least one number')
        return v

class LoginUser(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

class UpdateUser(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=20)
    username: Optional[str] = Field(None, min_length=2, max_length=50)
    password: Optional[str] = Field(None, min_length=8)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if re.search(r'[!@":;№()/|#$%^&*?]', v):
            raise ValueError('Name must not contain special characters')
        if " " in v:
            raise ValueError('Name must not contain spaces')
        return v

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if re.search(r'[!@":;№()/|#$%^&*?]', v):
            raise ValueError('Username must not contain special characters')
        if " " in v:
            raise ValueError('Username must not contain spaces')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Password must contain at least one letter')
        if " " in v:
            raise ValueError('Password must not contain spaces')
        if not re.search(r'[!@#$%^&*?]', v):
            raise ValueError('Password must not contain at least one special character !@#$%^&*?')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must not contain at least one number')
        return v

class OutputUser(BaseModel):
    id: int
    name: str
    username: str
    #password: str
    created_time: str

class CreateTask(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(None, max_length=300)
    status: int = Field(default=0)
    limit_time: str = Field(None)

    @field_validator('limit_time')
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            input = datetime.datetime.strptime(v, '%Y-%m-%d').date()
            current = datetime.date.today()
            if current > input:
                raise ValueError
        except ValueError:
            raise ValueError('Wrong format of data')
        return v

class UpdateTask(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    status: Optional[Literal[0,1]] = Field(None)
    limit_time: Optional[str] = Field(None)

    @field_validator('limit_time')
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            datetime.datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f'Wrong format of data')
        return v

class OutputTask(BaseModel):
    user_id: int
    id: int
    name: str
    description: Optional[str]
    status: int
    limit_time: Optional[str]
    created_time: str
