from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class Post(PostBase):
    pass

class PostRespone(PostBase):
    id: int
    create_at: datetime
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    create_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None