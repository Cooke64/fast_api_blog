from typing import List

from pydantic import BaseModel, EmailStr


class PostSchema(BaseModel):
    title: str
    text: str

    class Config:
        orm_mode = True


class UserOutForPost(BaseModel):
    username: str

    class Config:
        orm_mode = True


class PostOut(PostSchema):
    author_id: str
    author: UserOutForPost

    class Config:
        orm_mode = True

class CommentSchema(BaseModel):
    body: str