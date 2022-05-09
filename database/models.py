from datetime import datetime

from sqlalchemy import Column as _, Integer, String, ForeignKey, Boolean, Table, DateTime
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'
    id = _(Integer, primary_key=True, index=True)
    title = _(String)
    text = _(String)
    file_url = _(String, nullable=True)
    file_type = _(String, nullable=True)
    author_id = _(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="post", lazy=True)
    likes = relationship('Like', backref='post', lazy=True)
    created_at = _(DateTime, nullable=False, default=datetime.utcnow)
    comments = relationship('Comment', backref='post', lazy=True)


Follower = Table('followers',
                 Base.metadata,
                 _('user_id', Integer, ForeignKey('users.id')),
                 _('followed', Integer, ForeignKey('users.id'))
                 )


class User(Base):
    __tablename__ = 'users'
    id = _(Integer, primary_key=True, index=True)
    username = _(String, unique=True, nullable=False)
    email = _(String, unique=True, nullable=False)
    password = _(String, nullable=False)
    post = relationship("Post", back_populates="author")
    is_active = _(Boolean, default=True, nullable=False)
    is_superuser = _(Boolean, default=False, nullable=False)
    joined_at = _(DateTime, nullable=False, default=datetime.utcnow)
    followed = relationship(
        'User', secondary=Follower,
        primaryjoin=(Follower.c.user_id == id),
        secondaryjoin=(Follower.c.followed == id),
        backref='Подписчики',
        lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            return self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            return self.followed.remove(user)

    def is_following(self, user):
        """Проверка, является ли подписчиком."""
        if self.followed.filter(Follower.c.followed == user.id):
            return True


class Like(Base):
    """Лайки к посту."""
    __tablename__ = 'likes'
    id = _(Integer, primary_key=True)
    author = _(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = _(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)


class Comment(Base):
    """Комментарии к посту."""
    __tablename__ = 'comments'
    id = _(Integer, primary_key=True)
    body = _(String(199), nullable=False)
    created_at = _(DateTime, nullable=False, default=datetime.utcnow)
    post_id = _(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    user_id = _(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
