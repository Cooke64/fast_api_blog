from pydantic import BaseModel

from posts.schemes import UserOutForPost


class FollowerCreate(BaseModel):
    username: str


class FollowerList(BaseModel):
    user: UserOutForPost
    subscriber: UserOutForPost
