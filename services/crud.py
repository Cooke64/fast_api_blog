from fastapi.params import Depends
from sqlalchemy.orm import Session

from auth.hash_password import Hash
from auth.oayth2 import get_user
from database import get_db
from database.models import Post, User, Comment


class BaseCrud:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_item(self, item):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)


class PostCrud(BaseCrud):
    """CRUD для модели поста."""

    def find_all_posts(self):
        """Все посты."""
        query = self.db.query(Post).all()
        return query

    def get_post_by_id(self, post_id):
        """Получить пост по id."""
        query = self.db.query(Post)
        return query.filter(Post.id == post_id).first()

    def create_new_post(self, file_name, file_type, post, user: User = Depends(get_user)):
        """Создание нового поста. Дополнительные функции вынесение в post_services."""
        new_post = Post(file_url=file_name,
                        file_type=file_type,
                        author_id=user,
                        **post.dict()
                        )
        self.create_item(new_post)
        return new_post

    def change_post(self, post_id, request=None, update=False, user: User = Depends(get_user)):
        """Обновить пост по post_id."""
        post = self.get_post_by_id(post_id)
        if not post.author_id == user.id or user.is_superuser:
            pass
        query = self.db.query(Post)
        query.filter(Post.id == post_id).first()
        if update:
            query.update(request.dict())
            self.db.commit()
            return {f'post {post_id}': 'updated'}
        query.delete(synchronize_session=False)
        self.db.commit()
        return {'data': 'deleted'}

    def add_comment_to_post(self, response, post_id, user_id):
        """Добавить комментарий к посту."""
        comment = Comment(
            body=response.body,
            post_id=post_id,
            user_id=user_id,
        )
        self.create_item(comment)
        return comment


class UserCrud(BaseCrud):

    def create_new_user(self, request):
        password = Hash.bcrypt_password(request)
        new_user = User(
            username=request.username, email=request.email, password=password)
        self.create_item(new_user)
        return new_user

    def get_user_by_username(self, username: str):
        """Получить user по id."""
        query = self.db.query(User)
        return query.filter(User.username == username).first()
