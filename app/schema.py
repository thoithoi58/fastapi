from pydantic import BaseModel
from datetime import datetime

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

    class Config:
        orm_mode = True