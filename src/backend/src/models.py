from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
    id: Optional[int]
    content: str
    user_username: str
    date_created: Optional[datetime]
    date_store: Optional[datetime]

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: Optional[str]

    class Config:
        orm_mode = True

class User(BaseModel):
    username: str
    is_active: bool

    class Config:
        orm_mode = True

class Follow(BaseModel):
    id: Optional[int]
    follower_username: str
    following_username: str

    class Config:
        orm_mode = True
