import os
from pathlib import Path

from dotenv import load_dotenv
from starlette import status

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Yatube v.1.3"
    PROJECT_VERSION: str = "1.0.0"

    SQLALCHAMY_DATABASE_URL = 'sqlite:///./blog.db'

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    CREATED = status.HTTP_201_CREATED
    OK = status.HTTP_200_OK
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    DELETED = status.HTTP_204_NO_CONTENT
    ACCEPTED = status.HTTP_202_ACCEPTED


settings = Settings()
