from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from api.config import settings
from auth.make_token import create_access_token
from auth.oayth2 import get_user
from database import get_db
from database.models import User
from services.crud import UserCrud
from users.schemes import UserOutSchema, UserSchema, LoginUserSchema
from users.services import get_user_from_db

router = APIRouter(prefix='/user', tags=['Пользователи'])


@router.post('/login')
def login(request: LoginUserSchema, db: Session = Depends(get_db)):
    """Авторизация на сайт."""
    user = get_user_from_db(db, request)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/', status_code=settings.CREATED, response_model=UserOutSchema)
async def signup_user(request: UserSchema, user_service: UserCrud = Depends()):
    """Создание нового пользователя."""
    return user_service.create_new_user(request=request)


@router.get('/{username}', response_model=UserOutSchema)
async def get_user_detail(username: str, user_service: UserCrud = Depends()):
    """Получаем пользователя по его username."""
    return user_service.get_user_by_username(username)


@router.get('/me', response_model=UserOutSchema)
async def get_my_page(user_service: UserCrud = Depends(),
                      user: User = Depends(get_user)):
    """Получение данных текущего пользователя."""
    return user_service.get_user_by_username(username=user.username)
