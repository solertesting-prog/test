from fastapi import APIRouter, Query

from app.core.news.entities.news_article import NewsArticle
from app.core.news.services import news_article_service

from ..container import dependencies

router = APIRouter(
    prefix="/news",
    tags=["news"],
)
news_article_repository = dependencies().news_article_repository

# TODO: Add get news by category
# TODO: Add get news by id
# TODO: Add get news by user interests


@router.get("/")
async def get_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
) -> list[NewsArticle]:
    """Get all news articles."""
    news = await news_article_service.get_all_news_articles(
        news_article_repository, skip=skip, limit=limit
    )
    return news
