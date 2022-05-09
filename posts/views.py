from typing import List, Optional

from fastapi import APIRouter, Form, UploadFile, File
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks
from starlette.responses import StreamingResponse

from api.config import settings
from auth.oayth2 import get_user
from database import get_db
from database.models import User, Like, Comment
from posts.schemes import PostSchema, PostOut, CommentSchema
from posts.services import get_file_name
from services.crud import PostCrud

router = APIRouter(prefix='/posts', tags=['Посты'])


@router.post('/', status_code=settings.CREATED)
async def create_post(
        tasks: BackgroundTasks,
        title: str = Form(...),
        text: str = Form(...),
        item: Optional[UploadFile] = File(...),
        post_service: PostCrud = Depends()
):
    """Создает новый пост."""
    file_type = item.content_type
    file_name = get_file_name(file_type, tasks, item)
    post = PostSchema(title=title, text=text)
    return post_service.create_new_post(file_name, file_type, post)


@router.get('/', response_model=List[PostOut])
def get_posts(post_service: PostCrud = Depends()):
    """Получает список всех записей."""
    return post_service.find_all_posts()


@router.get('/{post_id}', status_code=settings.OK, response_model=PostOut)
async def get_post_detail(post_id: int, post_service: PostCrud = Depends()):
    """Получение записи по её post_id."""
    file = post_service.get_post_by_id(post_id=post_id)
    file_like = open(file.file_url, mode='rb')
    return StreamingResponse(file_like, media_type=f'{file.file_type}')


@router.delete('/{post_id}', status_code=settings.DELETED)
async def delete(post_id, post_service: PostCrud = Depends()):
    """Удаление записи по её post_id."""
    return post_service.change_post(post_id)


@router.put('/{post_id}', status_code=settings.ACCEPTED)
async def update_post(
        post_id: int, request: PostSchema,
        post_service: PostCrud = Depends(),
):
    """Обновление записи по её post_id."""
    return post_service.change_post(request=request, post_id=post_id,
                                    update=True)


@router.post("/add_like/{post_id}", status_code=settings.OK)
async def add_like(post_id: int, db: Session = Depends(get_db), user: User = Depends(get_user)):
    """Добавить лайк посту, если уже имеется лайк у данного юзера, то лайк удаляется."""
    like = db.query(Like).filter(
        Like.author == user, Like.post_id == post_id).first()
    if like:
        db.delete(like)
        db.commit()
    else:
        like = Like(author=user, post_id=post_id)
        db.add(like)
        db.commit()
    return {'done': 'success'}


@router.post("/add_comment/{post_id}", status_code=settings.OK)
async def add_comment(post_id: int, response: CommentSchema,
                      post_service: PostCrud = Depends(),
                      user: User = Depends(get_user)
                      ):
    """Добавить комментарий посту."""
    return post_service.add_comment_to_post(post_id=post_id, response=response,
                                            user_id=user)


@router.delete("/delete_comment/{comment_id}", status_code=settings.OK)
async def delete_comment(comment_id: int, db: Session = Depends(get_db),
                         user: User = Depends(get_user)):
    """Удалить комментарий к посту."""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment.user_id == user.id or user.is_superuser:
        pass
    db.delete(comment)
    db.commit()
    return {'Done': 'deleted'}
