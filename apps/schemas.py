from pydantic import BaseModel, EmailStr
from datetime import datetime 
from typing import Optional, List


class PostBase(BaseModel): 
    title: str
    content: str
    created_at: datetime
    published: bool = True

    class Config: 
        orm_mode = True

class PostCreate(PostBase): 
    pass

class UserOut(BaseModel): 
    id: int
    email: EmailStr
    created_at: datetime

class Post(PostBase): 
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class CreateUser(BaseModel): 
    email: EmailStr
    password: str



    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel): 
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None 

class Vote(BaseModel):
    post_id: int
    dir: int

class PostOut(BaseModel):
    post: Post
    votes: int 
    
    class Config:
        orm_mode = True
