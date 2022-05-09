from typing import List

from pydantic import BaseModel, EmailStr

from posts.schemes import PostSchema


class UserOutSchema(BaseModel):
    username: str
    email: EmailStr
    is_active: bool
    post: List[PostSchema] = []

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginUserSchema(BaseModel):
    username: str
    password: str
