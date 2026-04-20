from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    #id: int
    username: str
    name: str
    password: int
    #created_at: datetime

class OutputUser(BaseModel):
    username: str