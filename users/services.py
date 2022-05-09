from fastapi import HTTPException

from api.config import settings
from auth.hash_password import Hash
from database.models import User


def get_user_from_db(db, request):
    """Запрос на получение данных о текущем пользователе."""
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=settings.NOT_FOUND,
                            detail=f"Что-то неправильно")
    if not Hash.verify_password(user.password, request.password):
        raise HTTPException(status_code=settings.NOT_FOUND,
                            detail=f"Неправильный пароль")
    return user
