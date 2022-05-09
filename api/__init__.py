from fastapi import FastAPI

from posts import views as post_views
from users import views as user_views
from follow import views as follow_views
from database import models, engine


def get_application() -> FastAPI:
    app = FastAPI(
        title='Yatube 2.1',
        description='Третья версия проекта',
        version='1.0.0'
    )

    app.include_router(post_views.router)
    app.include_router(user_views.router)
    app.include_router(follow_views.router)

    models.Base.metadata.create_all(engine)
    return app


app = get_application()
