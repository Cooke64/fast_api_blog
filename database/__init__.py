from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.config import settings


engine = create_engine(
    settings.SQLALCHAMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        