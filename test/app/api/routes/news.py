from uuid import UUID
from fastapi import APIRouter, Query, HTTPException

from app.core.news.entities.news_article import NewsArticle
from app.core.news.services import news_article_service
from app.core.news.services.exceptions import NewsArticleNotFound

from ..container import dependencies

router = APIRouter(
    prefix="/news",
    tags=["news"],
)
news_article_repository = dependencies().news_article_repository

@router.get("/{id}")
async def get_news_by_id(
  id:UUID
) -> NewsArticle:
    """Get news by id."""
    try:
        news = await news_article_service.get_news_article_by_id(
            id=id,
            news_article_repository=news_article_repository
        )
        return news
    except NewsArticleNotFound:
        raise HTTPException(status_code=404, detail="News article not found")

@router.get("/")
async def get_news(
    category: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
) -> list[NewsArticle]:
    """Get all news articles."""
    news = await news_article_service.get_all_news_articles(
        news_article_repository, skip=skip, limit=limit,category=category
    )
    return news
