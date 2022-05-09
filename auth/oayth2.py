from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer

from api.config import settings
from auth.make_token import verify_token
from database.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=settings.NOT_FOUND,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    return verify_token(data, credentials_exception)


def get_user(current_user: User = Security(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_superuser(current_user: User = Security(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
