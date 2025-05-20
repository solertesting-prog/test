from .news import router as news_router
from .users import router as users_router
from fastapi import FastAPI

def build_routers(app: FastAPI) -> None:
    """Build the routers for the application.

    Args:
        app (FastAPI): FastAPI application instance
    """
    app.include_router(users_router)
    app.include_router(news_router)