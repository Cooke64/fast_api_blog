from typing import List

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from api.config import settings
from auth.oayth2 import get_user
from database import get_db
from database.models import User, Follower
from follow.schemas import FollowerList
from services.crud import UserCrud

router = APIRouter(tags=['Подписка'])


@router.post('/subscribe/{username}', status_code=settings.OK)
async def follow_user(username: str,
                      db: Session = Depends(get_db),
                      user_service: UserCrud = Depends(),
                      user: User = Depends(get_user)):
    """Добавление в подписчики"""
    item = user_service.get_user_by_username(username=username)
    if item is None:
        raise HTTPException(status_code=settings.NOT_FOUND, detail=f'Ничего не найдено')
    if user == item:
        raise HTTPException(status_code=settings.NOT_FOUND,
                            detail=f'Нельзя на себя подписаться!')
    user.follow(item)
    db.commit()
    return {'done': '!!!!'}


@router.post('/unsubscribe/{username}', status_code=settings.OK)
async def unfollow_user(username: str, db: Session = Depends(get_db),
                        user_service: UserCrud = Depends(),
                        user: User = Depends(get_user)):
    """Удаляем из подписчиков"""
    item = user_service.get_user_by_username(username=username)
    if item is None:
        raise HTTPException(status_code=settings.NOT_FOUND, detail=f'Ничего не найдено')
    user.unfollow(item)
    db.commit()
    return {'done': '!!!!'}


@router.get('/my_follow_list', response_model=List[FollowerList])
async def my_list_following(db: Session = Depends(get_db),
                            user: User = Depends(get_user)):
    """Список моих подписчиков."""
    return db.query(Follower).filter(Follower.c.followed == user).all()


@router.get('/my_followers', response_model=List[FollowerList])
async def my_list_follower(user: User = Depends(get_user),
                           db: Session = Depends(get_db)):
    """На кого я подписан."""
    return db.query(Follower).filter(Follower.c.user_id == user).all()
